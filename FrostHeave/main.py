#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pymysql
import numpy as np
import configparser
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import func, distinct
from sqlalchemy.dialects.mysql import DOUBLE
from sqlalchemy import create_engine, Column, Integer, String
from os import path
from sys import argv
from datetime import datetime, timedelta

CURRENT_DIR = path.dirname(path.realpath(argv[0])) + "\\"

input_table_mapper = {}

config = configparser.ConfigParser()
config.read(CURRENT_DIR + "setting.ini", encoding="utf-8")

host = config['mysql']['host'].strip()
username = config['mysql']['username'].strip()
password = config['mysql']['password'].strip()
port = config['mysql']['port'].strip()
database_name = config['mysql']['database'].strip()
import_file_name = config['import_file']['name'].strip()

NUM_SCALE = 6
MINI_EPS = 1e-6
mysql_config = 'mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8' % (username, password, host, port, database_name)
engine = create_engine(mysql_config, echo=False)

# expire_on_commit=False
Base = declarative_base()
DbSession = sessionmaker(bind=engine)
session = DbSession()


class InputDataModel:
    # 输入值：时间、轨温T_r、应变差值ε_d
    # 输出值：轨温、冻胀高度、锁定轨温、应力
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    date = Column(String(32), index=True)
    time = Column(String(32))
    temperature = Column(DOUBLE)
    strain = Column(DOUBLE)

    k_packet_num = Column(Integer)
    k = Column(DOUBLE)
    k0_packet_num = Column(Integer)
    k0 = Column(DOUBLE)
    k0_accumulate = Column(DOUBLE)
    mutation_accumulate = Column(DOUBLE)

    height = Column(DOUBLE)
    tsf = Column(DOUBLE)
    stress = Column(DOUBLE)


def fmt(x):
    if x is None:
        return 0.0
    else:
        return round(float(x), NUM_SCALE)


#   最小二乘法
def least_square(former_days_list):
    x = [fmt(data.temperature) for data in former_days_list]
    y = [fmt(data.strain) for data in former_days_list]
    x, y = np.array(x), np.array(y)
    a = np.polyfit(x, y, 1)
    return fmt(a[0])


def parse_time(date, time):
    year_s, mon_s, day_s = date.strip().split('/')
    h, m, s = time.strip().split(':')
    return datetime(int(year_s), int(mon_s), int(day_s), int(h), int(m), int(s))


def is_time_less3h(date, time, date2, time2):
    a = parse_time(date, time)
    b = parse_time(date2, time2)
    tmp = a - b
    return abs(tmp) < timedelta(hours=3)


def get_k_packet_num_by_date(days, InputDataClass):
    query_data = session.query(InputDataClass.date) \
        .order_by(InputDataClass.id.desc()) \
        .distinct(InputDataClass.date) \
        .limit(days)
    recent_days = [v[0] for v in query_data]
    recent_data_list = session.query(InputDataClass) \
        .filter(InputDataClass.date.in_(recent_days)) \
        .all()
    return least_square(recent_data_list), len(recent_data_list)


def get_k_by_packet_num(packet_num, InputDataClass):
    former_days_list = session.query(InputDataClass) \
        .order_by(InputDataClass.id.desc()) \
        .limit(packet_num)
    return least_square(former_days_list)


def get_k_k0(InputDataClass, flag_day_num, last_data, src_data):
    recorded_day_count = session.query(func.count(distinct(InputDataClass.date))).scalar()
    new_day = False
    if last_data.date != src_data.date:
        new_day = True
    acc_days = recorded_day_count + int(new_day)

    #   d > 16
    if acc_days > flag_day_num + 1:
        k = get_k_by_packet_num(last_data.k_packet_num, InputDataClass)
        return last_data.k0_packet_num, last_data.k0, last_data.k_packet_num, k, last_data.k0_accumulate
    #   3 <= d <= 16
    elif 3 <= acc_days <= flag_day_num + 1:
        #   3 <= d <= 16 new day
        if new_day:
            #   d = 3, 8, 16  new day
            if acc_days in [3, 8, 16]:
                k0 = 0
                k0_accumulate = 0
                k0_packet_num = 0
                if acc_days == 3:
                    k0, k0_packet_num = get_k_packet_num_by_date(2, InputDataClass)
                    k0_accumulate = 0
                elif acc_days == 8:
                    k0, k0_packet_num = get_k_packet_num_by_date(7, InputDataClass)
                    k0_accumulate = k0 - last_data.k0
                elif acc_days == 16:
                    k0, k0_packet_num = get_k_packet_num_by_date(15, InputDataClass)
                    k0_accumulate = k0 - last_data.k0 + last_data.k0_accumulate
                k_packet_num = k0_packet_num
                k = get_k_by_packet_num(k_packet_num, InputDataClass)
                return k0_packet_num, k0, k_packet_num, k, k0_accumulate
            #   d = 4, 5, 6, 7, 9, ... , 16 new day
            else:
                k_packet_num = last_data.k_packet_num + 1
                k = get_k_by_packet_num(k_packet_num, InputDataClass)
                return last_data.k0_packet_num, last_data.k0, k_packet_num, k, last_data.k0_accumulate

        #   3 < d <= 16 not new day
        else:
            if acc_days == 16:
                k = get_k_by_packet_num(last_data.k_packet_num, InputDataClass)
                return last_data.k0_packet_num, last_data.k0, last_data.k_packet_num, k, last_data.k0_accumulate
            else:
                k_packet_num = last_data.k_packet_num + 1
                k = get_k_by_packet_num(k_packet_num, InputDataClass)
                return last_data.k0_packet_num, last_data.k0, k_packet_num, k, last_data.k0_accumulate
    #   d < 3
    elif acc_days < 3:
        return None


def parser_form(data):
    if data is None:
        return None
    data.temperature = fmt(data.temperature)
    data.strain = fmt(data.strain)
    data.k0 = fmt(data.k0)
    data.k = fmt(data.k)
    data.k0_accumulate = fmt(data.k0_accumulate)
    data.mutation_accumulate = fmt(data.mutation_accumulate)
    return data


def get_param(src_data, InputDataClass):
    last_data = session.query(InputDataClass) \
        .order_by(InputDataClass.id.desc()) \
        .first()
    last_data = parser_form(last_data)
    if last_data is None:
        return None
    tmp = get_k_k0(InputDataClass, 15, last_data, src_data)
    if tmp is None:
        return None
    else:
        k0_packet_num, k0, k_packet_num, k, k0_accumulate = tmp
        mutation = (src_data.strain - last_data.mutation_accumulate - last_data.strain) -\
                   (k0 * (src_data.temperature - last_data.temperature))
        mutation = fmt(mutation)
        delta_t = abs(src_data.temperature - last_data.temperature)
        if delta_t < MINI_EPS:
            deviation = True
        else:
            deviation = abs(mutation / delta_t) - 180 > MINI_EPS

        truth = is_time_less3h(src_data.date, src_data.time, last_data.date, last_data.time) \
                and (abs(mutation) - 400 > MINI_EPS)  \
                and deviation

        if truth:
            return k0_packet_num, k0, k_packet_num, k, k0_accumulate, last_data.mutation_accumulate + mutation
        else:
            return k0_packet_num, k0, k_packet_num, k, k0_accumulate, last_data.mutation_accumulate


def compute_save(data, InputDataClass):
    #   更新参数 Mnemonic.param
    tmp = get_param(data, InputDataClass)
    # None : < 3 days
    if tmp is not None:
        k0_packet_num, k0, k_packet_num, k, k0_accumulate, mutation_accumulate = tmp
        data.height = fmt((-k + k0 - k0_accumulate) * 0.5 + mutation_accumulate * 0.0189)
        data.tsf = fmt((-k + k0 - k0_accumulate) * 0.6 + 10 + mutation_accumulate * 0.08475)
        data.strain -= mutation_accumulate

        data.stress = fmt(0.21 * 11.8 * (data.temperature - data.tsf))

        data.k0 = k0
        data.k0_packet_num = k0_packet_num
        data.k0_accumulate = k0_accumulate
        data.k = k
        data.k_packet_num = k_packet_num

        data.mutation_accumulate = mutation_accumulate

    print_str = "%s|%s|%s|%s|%s|%s" % (InputDataClass.__tablename__, data.date, data.time,
                                       data.height, data.tsf, data.stress)
    print(print_str)
    session.add(data)
    session.flush()


def mapper_generate(table_mapper_dict, Model, device_name, table_prefix):
    table_name = '%s_%s' % (table_prefix, device_name)
    if table_name not in table_mapper_dict:
        table_mapper_dict[table_name] = type(
            table_name,
            (Model, Base),
            {'__tablename__': table_name}
        )
    return table_mapper_dict[table_name]


def generate_class(device_name: str):
    device_name = device_name.lower()
    input_tmp = mapper_generate(input_table_mapper, InputDataModel, device_name, "ef_statistics")
    return input_tmp


def get_data(tmp, InputDataClass):
    return InputDataClass(date=tmp[1], time=tmp[2], temperature=fmt(tmp[3]), strain=fmt(tmp[4]))


def get_data_str(line):
    tmp = line.strip().split('|')
    return [x.strip() for x in tmp]


def read_from_file(InputDataClass):
    global import_file_name
    text_list = []
    with open(CURRENT_DIR + import_file_name, 'r', encoding="utf-8") as f:
        while True:
            line = f.readline()
            if not line:
                break
            text_list.append(line)
    data_list = []
    try:
        for line in text_list:
            str_list = get_data_str(line)
            data_list.append(get_data(str_list, InputDataClass))
    except Exception as e:
        print(e)
        print("注意当前也许存在的格式问题")
    return data_list


def deal_by_cmd():
    tmp = get_data_str(argv[1])
    InputDataClass = generate_class(tmp[0])
    Base.metadata.create_all(engine)
    #   拿到最新参数
    data = get_data(tmp, InputDataClass)
    compute_save(data, InputDataClass)


def deal_by_file():
    device_name = config['import_file']['device'].strip()
    InputDataClass = generate_class(device_name)
    Base.metadata.create_all(engine)

    import_file_list = read_from_file(InputDataClass)
    #   拿到最新参数
    for i in range(len(import_file_list)):
        print("====== 文本输入模式 ======")
        print("从文件 %s 处理设备 %s 的数据" % (import_file_name, device_name))
        print("正在处理第 %d 包数据" % (i + 1))
        compute_save(import_file_list[i], InputDataClass)


def class_init_by_config():
    devices = config['mysql']['devices'].strip().split(',')
    devices = [name.strip() for name in devices]
    for device_name in devices:
        generate_class(device_name)


def main():
    class_init_by_config()
    if len(argv) != 2:
        print("参数无效")
    if argv[1] == "-f":
        deal_by_file()
    else:
        deal_by_cmd()


if __name__ == '__main__':
    main()
    session.commit()
    session.close()

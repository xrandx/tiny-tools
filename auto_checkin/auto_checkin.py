# -*- coding: utf-8 -*-
# author: xrandx

import requests
import json
import time
import os
from requests.packages import urllib3


BASE_URL = r"https://blue7.fun/"
ERROR = 0
CORRECT = 1
ERROR_CHECK_IN_OUT = r"您似乎已经签到过了..."
ERROR_COIN_OVERFLOW = r"硬币上限1000，无法签到"
ERROR_TIMEOUT = r"到期用户无法签到，请先兑换时间"

headers = {
    'User-Agent': 'Mozilla/5.0',
    'Connection': 'Keep-Alive'
}


re_data = {
    'coupon': "Blue_7_acess_1077",
    'shop': "1",
    'autorenew': 1
}

bestbuy_data = {
    'shop': "26"
}


def login(login_data):
    s = requests.Session()
    r = s.post(BASE_URL + r"auth/login", data=login_data, headers=headers, verify=False)
    json_data = json.loads(r.text)
    if json_data["ret"] == ERROR:
        print("发生未知登录错误，请检查账号和密码。")
    else:
        print(json_data["msg"])
    time.sleep(3)
    return s


def check_in(s):
    r = s.post(BASE_URL + r"user/checkin", headers=headers, verify=False)
    json_data = json.loads(r.text)
    if json_data["msg"] == ERROR_CHECK_IN_OUT:
        print(ERROR_CHECK_IN_OUT)
    elif json_data["msg"] == ERROR_TIMEOUT:
        print("兑换码已经到期，将自动填报")
        buy_time(s)
    elif json_data["msg"] == ERROR_COIN_OVERFLOW:
        print(ERROR_COIN_OVERFLOW)
        buy_best_package(s)
    else:
        print("签到成功")
        print(json_data["msg"])


def buy_time(s):
    print("正在发送兑换码...")
    r = s.post(BASE_URL + r"user/coupon_check", data=re_data, headers=headers, verify=False)
    r = s.post(BASE_URL + r"user/buy", data=re_data, headers=headers, verify=False)
    json_data = json.loads(r.text)
    print(json_data["msg"])
    check_in(s)


def buy_best_package(s):
    print("正在购买最佳套餐...")
    r = s.post(BASE_URL + r"user/coupon_check", data=bestbuy_data, headers=headers, verify=False)
    json_data = json.loads(r.text)
    print("将购买套餐：" + json_data['name'] + ' ' + json_data['credit'] + ' ' + json_data['total'])
    r = s.post(BASE_URL + r"user/buy", data=bestbuy_data, headers=headers, verify=False)
    print(json.loads(r.text)["msg"])
    check_in(s)


def main():
    urllib3.disable_warnings()
    print("blue.fun签到助手")
    print('================')
    print("")
    login_arr = []
    with open('user_list.txt', 'r') as f:
        print("打开并读取账号记录")
        while True:
            login_data = {}
            email = f.readline().strip()
            passwd = f.readline().strip()
            if not passwd:
                break
            login_data['email'] = email
            login_data['passwd'] = passwd
            login_arr.append(login_data)
            print("收录 " + email)
    print('----------------')
    for login_data in login_arr:
        print(login_data["email"] + "正在签到。")
        check_in(login(login_data))
        print('----------------')
    with open('user_list.txt', 'w') as f:
        for i in login_arr:
            f.write(i["email"] + "\n" + i["passwd"] + "\n")
    while True:
        message = input("请按任意键，输入回车退出")
        if message != "":
            break


if __name__ == '__main__':
    main()


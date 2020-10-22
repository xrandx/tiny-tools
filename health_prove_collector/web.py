# -*- coding: utf-8 -*-
from flask import Flask, render_template, session, jsonify, redirect, request, url_for, send_from_directory, abort, json
from os.path import split, realpath, join, getsize
import mysql.connector
from os import listdir, rename, chdir, remove
from zipfile import ZipFile
import datetime
from pypinyin import lazy_pinyin
from werkzeug.utils import secure_filename


application = Flask(__name__)
application.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

application.config['JSON_AS_ASCII'] = False
application.jinja_env.block_start_string = '(%'  # 修改块开始符号
application.jinja_env.block_end_string = '%)'  # 修改块结束符号
application.jinja_env.variable_start_string = '((_'  # 修改变量开始符号
application.jinja_env.variable_end_string = '_))'  # 修改变量结束符号
application.jinja_env.comment_start_string = '(#'  # 修改注释开始符号
application.jinja_env.comment_end_string = '#)'  # 修改注释结束符号
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'tif', 'zip'}

PROGRAM_DIR = split(realpath(__file__))[0] + "/"

db = mysql.connector.connect(
    host="localhost",  # 数据库主机地址
    # host="39.106.226.12",
    user="toys",  # 数据库用户名
    port='3306',
    passwd="3J65GANTMGtw275Y",  # 数据库密码
    database="toys"
)

name_dict = {}


def database_start():
    global name_dict
    cursor = db.cursor()
    cursor.execute("SELECT name, id, dept FROM 16Ji;")
    result = cursor.fetchall()
    for i in result:
        name = i[0].decode('utf-8')
        name_dict[name] = (i[1].decode('utf-8'), i[2].decode('utf-8'))


@application.route('/download')
def download():
    return render_template('download.html')


@application.route('/download/file')
def download_file():
    compressed_file = datetime.date.today().strftime("%m-%d") + '.zip'
    with ZipFile(PROGRAM_DIR + "static/" + compressed_file, "w") as myzip:
        file_array = listdir(PROGRAM_DIR + "static/uploads")
        chdir(PROGRAM_DIR + "static/uploads")
        for file in file_array:
            myzip.write(file)
            remove(file)
    addr = "/static/" + compressed_file
    return jsonify(addr)


@application.route('/forget')
def forget():
    global name_dict
    database_start()
    file_array = listdir(PROGRAM_DIR + "static/uploads")
    forget_list = list()
    for zw_name in name_dict.keys():
        flag = False
        for file_name in file_array:
            if zw_name in file_name:
                flag = True
                break
        if not flag:
            forget_list.append({"forget_name": zw_name})
    return jsonify(forget_list)


@application.route('/')
def index():
    database_start()
    return render_template('index2.html')


@application.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        f = request.files.get('file')
        json_data = request.form["data"]
        name = json.loads(json_data)["name"]
        filename = secure_filename(f.filename)
        idx = filename.rindex(".")
        filename = name + filename[idx:]
        upload_path = join(PROGRAM_DIR, "static/uploads/", filename)
        f.save(upload_path)
        return jsonify("static/uploads/" + filename)


if __name__ == '__main__':
    application.run()

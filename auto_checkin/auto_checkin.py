# -*- coding: utf-8 -*-
import requests
import json
import os

s = requests.Session()
BASE_URL = r"https://blue7.fun/"

headers = {
    'User-Agent': 'Mozilla/5.0',
    'Connection': 'Keep-Alive'
}

login_data = {
    'email': "1635699825@qq.com",
    'passwd': "15869844463"
}

shop_data = {
    'coupon': "Blue_7_acess_1077",
    'shop': "1"
}


def check_in():
    try:
        r = s.post(BASE_URL + r"auth/login", data=login_data, headers=headers)
        r = s.post(BASE_URL + r"user/checkin", headers=headers)
    except:
    str = r.text
    json_data = json.loads(str)
    if(json_data["msg"] == "\u60a8\u4f3c\u4e4e\u5df2\u7ecf\u7b7e\u5230\u8fc7\u4e86..."):
        print("失败")
        print(json_data["msg"])
    else:
        print(json_data["msg"])

print("你的账号是"+ login_data["email"])
check_in()
os.system('pause')



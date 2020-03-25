# -*- coding: UTF-8 -*-
# 大多为了方便采用全局变量
import json
import re

import pdfkit
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from random import choice, randint
import xlsxwriter
from os import listdir, system, makedirs
from os.path import exists, isfile
from time import sleep
import schedule
import os

CURRENT_DIR = os.path.split(os.path.realpath(__file__))[0] + "\\"
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('headless')
prefs = {
    "profile.managed_default_content_settings.images":2,
    'profile.managed_default_content_settings.javascript': 2,
    "permissions.default.stylesheet": 2,
}

chrome_options.add_experimental_option("prefs",prefs)
session = webdriver.Chrome(CURRENT_DIR + "chromedriver.exe", chrome_options=chrome_options)
wait = WebDriverWait(session, 30, 0.5)


def save_html():
    content = wait.until(EC.visibility_of_element_located((By.ID, "essay-body")))
    title = session.title[:-9]
    title = re.sub('[\/:*?"<>|]', '_', title)
    file_name = title + ".html"
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(content.get_attribute('innerHTML'))
        print(title + " 保存")


def start():
    with open("tmp.txt", "r", encoding="utf-8") as f:
        cnt = int(f.readline())
        print("读取%d页" % cnt)
    return cnt


def complete(cnt):
    with open("tmp.txt", "w", encoding="utf-8") as f:
        f.write("%d" % cnt)


def main():
    URL = "https://chuansongme.com/account/bitsea?start="
    cnt = 0
    cnt = start()
    old = 0
    PAGE_SIZE = 12
    END = 91
    flag = 0
    while cnt // PAGE_SIZE <= END:
        try:
            old = cnt
            page_num = (cnt // PAGE_SIZE) * PAGE_SIZE
            size = cnt - page_num
            session.get(URL + "%d" % page_num)
            elems = wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "question_link")))
            links = [elem.get_attribute('href') for elem in elems]
            links = links[size:]
            for link in links:
                js = "window.open(' %s')" % link
                session.execute_script(js)
                session.switch_to.window(session.window_handles[1])
                # wait.until(EC.presence_of_element_located((By.ID, "js_content")))
                save_html()
                session.close()
                session.switch_to.window(session.window_handles[0])
                cnt += 1
                complete(cnt)
        except Exception as e:
            session.close()
            session.switch_to.window(session.window_handles[0])
            if old == cnt:
                flag += 1
                if flag >= 2:
                    cnt += 1
                    flag = 0
            complete(cnt)
            print(e)

    # cmd = "shutdown -s -t 1"
    # system(cmd)

if __name__ == '__main__':
    main()


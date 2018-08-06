# 需要安装 openpyxl, pandas, BeautifulSoup
# pip install 即可


import requests
import re
import pandas as pd
from bs4 import BeautifulSoup

region = ['ganjingzi', 'shahekou', 'zhongshan', 'xigang', 'gaoxinyuanqu']
#这个变量里放区域名称的拼音
regnam = ['甘井子', '沙河口', '中山', '西岗', '高新园']#这个变量里放区域名称的中文
page = 5
reTryTime = 5
price=[]   #这个变量里放房屋总价
uprice=[]  #这个变量里放房屋均价
house=[]   #这个变量里放房屋信息
room=[]
area=[]
direct=[]
decorate=[]
elevator=[]


def generate_allurl(page):
    url = 'http://dl.lianjia.com/ershoufang/{}/pg{}/'
    # 改url换城市
    for url_region in range(len(region)):
        print("\n开始爬取地区："+ regnam[url_region] + "\n")
        for url_next in range(1,int(page) + 1):
            print("正在爬取第"+ str(url_next) + "页")
            yield url.format(region[url_region], url_next)


def get_allurl(generate_allurl):
    gotData = False 
    reTry = 0
    while reTry < reTryTime and not gotData: 
        try: 
            reTry += 1 
            get_url = requests.get(generate_allurl, timeout=1)
            if get_url.status_code == 200:
                re_set = re.compile('<li.*?class="clear">.*?<a.*?class="img.*?".*?href="(.*?)"')
                re_get = re.findall(re_set,get_url.text)
                gotData = True 
                return re_get
        except: 
            pass



def open_url(re_get):
    gotData = False 
    reTry = 0
    while reTry < reTryTime and not gotData: 
        try: 
            reTry += 1 
            res = requests.get(re_get, timeout=1)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text,'lxml')
                price.append(soup.select('.total')[0].text + '万')
                uprice.append(soup.select('.unitPriceValue')[0].text)
                house.append(soup.select('.communityName > a')[0].text)
                room.append(soup.find("div", class_="room").find("div", class_="mainInfo").text)
                area.append(soup.find("div", class_="area").find("div", class_="mainInfo").text)
                direct.append(soup.find("div", class_="type").find("div", class_="mainInfo").text)
                decorate.append(soup.find("div", class_="introContent").find_all("li")[8].text[4:])
                elevator.append(soup.find("div", class_="introContent").find_all("li")[11].text[4:])
                gotData = True
        except: 
            pass





def toTxt():
    print("\n开始保存txt文件……\n")
    for regnum in range(len(region)):
        print("录入" + regnam[regnum] + "数据")
        with open(regnam[regnum] + '.txt', 'w') as f:  # 建立并打开一个txt文件
            for i in range(len(price)):  # 建立一个循环
                f.write(str(price[i]) + ' | ' + str(uprice[i]) + ' | ' + str(house[i]) + ' | ' + str(room[i]) + ' | ' + str(area[i]) + ' | ' + str(direct[i]) + ' | ' + str(decorate[i]) + ' | ' + str(elevator[i]) +'\n')  # 将房屋总价写入txt文件
        print('已保存为 ' + regnam[regnum] + '.txt ')
    

def toXls():
    print("\n开始将所有地区数据保存为xls文件……\n")
    df = pd.DataFrame({
        "总价": price,
        "每平米均价": uprice,
        "房屋名称": house,
        "格局": room,
        "面积": area,
        "朝向": direct,
        "装修": decorate,
        "电梯": elevator
    })
    df.to_excel('大连链家二手房.xlsx',sheet_name='大连链家二手房')
    print("已保存为 大连链家二手房.xlsx")

def main():
    page = input('输入各地区生成页数：')
    print()
    for i in generate_allurl(page):
        print(i)
        url_tmp = get_allurl(i)
        for j in url_tmp:
            info = open_url(j)
    toTxt()
    print()
    toXls()
    print("完成")


if __name__ == '__main__':
    main()



# def get_allurl(generate_allurl):
#     get_url = requests.get(generate_allurl,)
#     if get_url.status_code == 200:
#         re_set = re.compile('<li.*?class="clear">.*?<a.*?class="img.*?".*?href="(.*?)"')
#         re_get = re.findall(re_set,get_url.text)
#         return re_get


# def open_url(re_get):
#     res = requests.get(re_get, timeout=0.1)
#     if res.status_code == 200:
#         soup = BeautifulSoup(res.text,'lxml')
#         price.append(soup.select('.total')[0].text + '万')
#         uprice.append(soup.select('.unitPriceValue')[0].text)
#         house.append(soup.select('.communityName > a')[0].text)
#         room.append(soup.find("div", class_="room").find("div", class_="mainInfo").text)
#         area.append(soup.find("div", class_="area").find("div", class_="mainInfo").text)
#         direct.append(soup.find("div", class_="type").find("div", class_="mainInfo").text)
#         decorate.append(soup.find("div", class_="introContent").find_all("li")[8].text[4:])
#         elevator.append(soup.find("div", class_="introContent").find_all("li")[11].text[4:])

  
import requests
import os
from PIL import Image
import pytesseract
import re
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

CAPTCHA_NUM = 100
s = requests.Session()  # 保持会话状态，使得进入选课界面，验证码依然有效
threshold = 127.5
threshold0 = 225.0
threshold1 = 115.0


# X = []
# Y = []
# Z = []


url = ["http://211.87.126.37", "http://211.87.126.78", "http://211.87.126.77","http://211.87.126.76/"]

headers = {
    'User-Agent': 'Mozilla/5.0',
    'Connection': 'Keep-Alive'
}


def get_all():
    if not os.path.exists(r'captcha_pic'):
        os.makedirs(r'captcha_pic')
    for i in range(CAPTCHA_NUM):
        filename = 'captcha_' + str(i) + ".png"
        #写入验证码
        r = s.get(url[1] + r'/validateCodeAction.do', headers=headers)
        img = r.content
        print(filename)
        f = open(r'captcha_pic/' + filename, 'wb')
        f.write(img)
        f.close()


def get_binary(f):
    image = Image.open(f, "r")
    image = image.convert('L')
    pixels = image.load()
    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')
    # for x in range(image.width):
    #     for y in range(image.height):
    #         if pixels[x, y] > threshold:
    #             pixels[x, y] = 255
    #         else:
    #             pixels[x, y] = 0

    for x in range(image.width):
        for y in range(image.height):
            # X.append(x)
            # Y.append(y)
            z = pixels[x, y]
            if 140 <= z <= 256:
                z = 255.0
                # Z.append(z)
            # else:
                # z = 0
                # Z.append(z)
            pixels[x, y] = z

    # ax.plot_trisurf(X, Y, Z)
    # plt.show()

    return image
    # for x in range(image.width):
    #     for y in range(image.height):
    #         if pixels[x, y] < threshold0:
    #             pixels[x, y] = 64
    #         elif pixels[x, y] <= threshold1:
    #             pixels[x, y] = 128
    #         elif pixels[x, y] <= threshold2:
    #             pixels[x, y] = 255
    #         else:
    #             pixels[x, y] = 0
    # return image


def change_img2txt(img):
    testdata_dir_config = '--tessdata-dir "C:\\Softwares\\Tesseract-OCR\\tessdata"'
    # textCode = pytesseract.image_to_string(img,lang='eng', config=testdata_dir_config)
    textCode = pytesseract.image_to_string(img,lang='eng', config="-c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ -psm 6")
    textCode = re.sub("\W", "", textCode)
    return textCode


def change_all():
    os.chdir("captcha_pic/")
    # print("目录为: %s" % os.listdir(os.getcwd()))
    for i in range(CAPTCHA_NUM):
        srcfile = 'captcha_' + str(i) + ".png"
        print(srcfile)
        f = open(srcfile, 'rb')
        img = get_binary(f)
        img.save("grey_" + srcfile)
        dstfile = change_img2txt(img) + ".png"
        print(dstfile)
        f.close()

        if len(dstfile) != 8 and os.path.exists(srcfile):
            print(len(dstfile))
            os.remove(srcfile)
            print('Destination file name is illegal, remove file success')
            os.rename(srcfile, dstfile)
            print("shit, wrong answer")
            print("----------------------")
        else:
            try:
                os.rename(srcfile, dstfile)
            except Exception as e:
                print('rename file fail')
            else:
                print('rename file success')


def main():
    get_all()
    change_all()


if __name__ == '__main__':
    main()
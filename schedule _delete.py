import os
import shutil
import re
CURRENT_DIR = os.path.split(os.path.realpath(__file__))[0] + "\\"

def main():
    path = ""
    mod_dic = ""
    with open( CURRENT_DIR + "setting.txt", "r", encoding="UTF-8-sig") as f:
        path = f.readline()
        mod_dic = f.readline()
        # with open( CURRENT_DIR + "setting.txt", "r", encoding="UTF-8") as f:
        #     path = f.readline()
        #     mod_dic = f.readline()
    path = path.replace("\\", "\\\\")
    path = path.strip()
    mod_dic = mod_dic.strip()
    print("---删除除了" + mod_dic + "之外的"+ path + "下的所有文件夹和文件---")
    dirs = os.listdir(path)
    if mod_dic not in dirs:
        print(mod_dic + "文件夹不存在")
        input("请在本程序目录新建setting.txt，第一行是待删除文件夹绝对路径，第二行是此文件夹下不需删除的文件夹名字")
    else:
        for file in dirs:
            if not (file in mod_dic and mod_dic in file):
                file_path = path + r"\\" + file
                if os.path.isfile(file_path):
                    print("删除了 " + file)
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    print("删除了 " + file)
                    shutil.rmtree(file_path, True)


if __name__ == '__main__':
    main()
from os import listdir, system, makedirs
from os.path import exists, isfile
import os
import img2pdf


CURRENT_DIR = os.path.split(os.path.realpath(__file__))[0] + "\\"



def main():
    os.chdir(CURRENT_DIR)  
    L = listdir()
    L = [i for i in L if i[-3:] == "jpg"]
    with open("name.pdf","wb") as f:
        f.write(img2pdf.convert(L))

if __name__ == '__main__':
    main()

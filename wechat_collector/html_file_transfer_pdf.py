from os import listdir, system, makedirs
from os.path import exists, isfile
import os
import pdfkit
import re

CURRENT_DIR = os.path.split(os.path.realpath(__file__))[0] + "\\"
options = {
    'page-size': 'Letter',
    'margin-top': '0.75in',
    'margin-right': '0.75in',
    'margin-bottom': '0.75in',
    'margin-left': '0.75in',
    'encoding': "UTF-8",  #支持中文
    'custom-header' : [
        ('Accept-Encoding', 'gzip')
    ],
    "no-images":None
}

if __name__ == "__main__":
    os.chdir(CURRENT_DIR)  
    L = listdir()
    L = sorted(L,  key=lambda x: os.path.getctime(os.path.join(CURRENT_DIR, x)), reverse=True)
    L = [i for i in L if i[-4:] == "html"]
    pattern=r'[\\/:*?"<>|\r\n]+'

    for i in L[1050:]:
        print(i)
        pdfkit.from_file(i, ".\\pdf\\" + i[:-5] + ".pdf", options=options)

    # for i in L:
    #     print(i)
        # if i[-4:] == "html":
        #     print(i)
        #     pdfkit.from_file(CURRENT_DIR + i, CURRENT_DIR + "pdf\\" +i[:-5] + '.pdf', options=options)
        #     break

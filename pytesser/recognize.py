#coding=utf-8


from pytesser import *  
import os

import urllib  
import urllib2  
import cookielib  
from StringIO import StringIO
# 二值化  
threshold = 140  
table = []  
for i in range(256):  
    if i < threshold:  
        table.append(0)  
    else:  
        table.append(1)  

def valid_text(text):
    if 'I' in text:
        return False
    if 'J' in text:
        return False
    if 'O' in text:
        return False
    return True


def getverify(url, request_session):
    text = ''
    cj = None
    while True:
        os.chdir(os.path.split(os.path.realpath(__file__))[0])
        name = 'check.jpg'
        res = request_session.get("http://uems.sysu.edu.cn/jwxt/jcaptcha", stream=True)
        open(os.path.split(os.path.realpath(__file__))[0] + '/check.jpg','wb').write(res.content)
        im = Image.open(name)
        #转化到亮度
        imgry = im.convert('L')
        #二值化
        out = imgry.point(table,'1')

        #裁剪
        box =(3, 3, out.size[0]-3, out.size[1]-3)#裁掉最下面24px

        out=out.crop(box)

        #识别
        text = image_to_string(out)
        #识别对吗
        text = text.replace(' ', '')
        text = text.replace(']', 'J')
        text = text.replace('!', 'I')
        text = text.replace('\n', '')
        text = text.upper()
        if valid_text(text):
            break

    return text



#getverify()  

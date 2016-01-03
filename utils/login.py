# -*- coding: utf-8 -*-
#!/usr/bin/env python

from pytesser.recognize import getverify
import hashlib
from bs4 import BeautifulSoup

class LoginStatus:
    UNKNOW = 1
    SUCCESS = 2
    PASSWORD_ERROR = 3
    CAPTCHA_ERROR = 4

def md5(psw):
    m = hashlib.md5()
    m.update(psw)
    return m.hexdigest().upper()

def login(username, password, request_session):
    res = request_session.get(
            "http://uems.sysu.edu.cn/jwxt",
            headers={'User-agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'})
    soup = BeautifulSoup(res.content.decode("utf-8"), "html.parser")
    rno = soup.find(id='rno')['value']
    chaptcha = getverify('http://uems.sysu.edu.cn/jwxt/jcaptcha', request_session)
    res = request_session.post("http://uems.sysu.edu.cn/jwxt/j_unieap_security_check.do", data={
                                  "j_username": username,
                                  "j_password": md5(password),
                                  "jcaptcha_response": chaptcha,
                                  "rno": rno,
                              })
    str = res.content.decode("utf-8")
    status = LoginStatus.UNKNOW
    #print str
    if u"页面正在加载" in str:
        status = LoginStatus.SUCCESS
    elif u"用户名不存在或密码错误" in str:
        status = LoginStatus.PASSWORD_ERROR
    elif u"错误的验证码" in str:
        status = LoginStatus.CAPTCHA_ERROR
    return status
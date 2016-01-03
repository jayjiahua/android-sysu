# -*- coding: utf-8 -*-
#!/usr/bin/env python

import requests
from login import login, LoginStatus

SESSION_DICT = {}
MAX_RETRY_TIME = 10

class Session:
    def new_session(self):
        return requests.Session()

    def save_session(self, token, username, password):
        #print session.cookies
        SESSION_DICT[token] = {
            "username": username,
            "password": password
        }

    def get_session(self, token):
        session = SESSION_DICT.get(token)
        if not session:
            return None
        n_session = self.new_session()
        status = login(session["username"], session["password"], n_session)
        time = 0
        while status == LoginStatus.CAPTCHA_ERROR or status == LoginStatus.UNKNOW and time < MAX_RETRY_TIME:
            status = login(session["username"], session["password"], n_session)
            time += 1

        return n_session

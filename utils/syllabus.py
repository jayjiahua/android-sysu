# -*- coding: utf-8 -*-
#!/usr/bin/env python

from bs4 import BeautifulSoup

def get_syllabus(year, term, request_session, ret_type):
    request_head = {
        'Accept': '*/*',
        'ajaxRequest': 'true',
        'render': 'unieap',
        '__clientType': 'unieap',
        'workitemid': 'null',
        'resourceid': 'null',
        'Content-Type': 'multipart/form-data',
        'Referer': 'http://uems.sysu.edu.cn/jwxt/sysu/xk/xskbcx/xskbcx.jsp?xnd=2014-2015&xq=1',
        'Accept-Language': 'zh-Hans-CN, zh-Hans; q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.3; WOW64; Trident/7.0; .NET4.0E; .NET4.0C; .NET CLR 3.5.30729; .NET CLR 2.0.50727; .NET CLR 3.0.30729)',
        'Host': 'uems.sysu.edu.cn',
        'Content-Length': 147,
        'Connection': 'Keep-Alive',
        'Pragma': 'no-cache'
    }
    request_body = {
        "header": {
            "code": -100,
            "message": {
                "title": "",
                "detail": ""
            }
        },
        "body": {
            "dataStores": {},
            "parameters": {
                "args": [
                    "%s" % term,
                    "%s-%s" % (year, year + 1),
                ],
                "responseParam": "rs"
            }
        }
    }
    res = request_session.post("http://uems.sysu.edu.cn/jwxt/KcbcxAction/KcbcxAction.action?method=getList",
                           headers=request_head, json=request_body)
    res_dict = eval(res.content, type('Dummy', (dict,), dict(__getitem__=lambda s,n:n))())
    if ret_type == "html":
        return res_dict['body']['parameters']['rs']
    else:
        ret = []
        soup = BeautifulSoup(res_dict['body']['parameters']['rs'], "html.parser")
        tr_list = soup.find_all("tr")
        for tr_tag in tr_list:
            td_list = tr_tag.find_all("td")
            week_day = 0
            for td_tag in td_list:
                if td_tag.get('rowspan'):
                    td_str = td_tag.prettify().split('\n')
                    if "<br>" in td_str[3]:
                        td_str.insert(3, u"待定")
                    ret.append({
                        "year": year,
                        "term": term,
                        "name": td_str[1].strip(),
                        "place": td_str[3].strip(),
                        "fromTime": int(td_str[5].strip()[:-1].split('-')[0]),
                        "toTime": int(td_str[5].strip()[:-1].split('-')[1]),
                        "week": td_str[7].strip(),
                        "day": week_day,
                    })
                week_day += 1
        return ret


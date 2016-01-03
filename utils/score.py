# -*- coding: utf-8 -*-
#!/usr/bin/env python

def get_score(year, term, request_session):
    request_head = {
        'Accept': '*/*',
        'ajaxRequest': 'true',
        'render': 'unieap',
        '__clientType': 'unieap',
        'workitemid': 'null',
        'resourceid': 'null',
        'Content-Type': 'multipart/form-data',
        'Referer': 'http://uems.sysu.edu.cn/jwxt/forward.action?path=/sysu/xscj/xscjcx/xsgrcj_list',
        'Accept-Language': 'zh-Hans-CN, zh-Hans; q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.3; WOW64; Trident/7.0; .NET4.0E; .NET4.0C; .NET CLR 3.5.30729; .NET CLR 2.0.50727; .NET CLR 3.0.30729)',
        'Host': 'uems.sysu.edu.cn',
        'Content-Length': 726,
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
            "dataStores": {
                "kccjStore": {
                    "rowSet": {
                        "primary": [],
                        "filter": [],
                        "delete": []
                    },
                    "name": "kccjStore",
                    "pageNumber": 1,
                    "pageSize": 2147483647,
                    "recordCount": 1,
                    "rowSetName": "pojo_com.neusoft.education.sysu.xscj.xscjcx.model.KccjModel",
                    "order": "t.xn, t.xq, t.kch, t.bzw"
                }
            },
            "parameters": {
                "kccjStore-params": [
                    {
                        "name": "Filter_t.pylbm_0.952770574354267",
                        "type": "String",
                        "value": "'01'",
                        "condition": " = ",
                        "property": "t.pylbm"
                    },
                    {
                        "name": "Filter_t.xn_0.5417678801132191",
                        "type": "String",
                        "value": "'%s-%s'" % (year, year + 1),
                        "condition": " = ",
                        "property": "t.xn"
                    },
                    {
                        "name": "Filter_t.xq_0.4146100189162235",
                        "type": "String",
                        "value": "'%s'" % (term),
                        "condition": " = ",
                        "property": "t.xq"
                    }
                ],
                "args": [
                    "student"
                ]
            }
        }
    }
    res = request_session.post("http://uems.sysu.edu.cn/jwxt/xscjcxAction/xscjcxAction.action?method=getKccjList",
                           headers=request_head, json=request_body)
    res_dict = eval(res.content, type('Dummy', (dict,), dict(__getitem__=lambda s,n:n))())
    return [{
            'year': year,
            'term': term,
            'name': c['kcmc'],
            'rank': c['jxbpm'].replace('\\', ''),
            'credit': c['xf'],
            'score': c['zzcj'],
            'courseId': c['kch'],
            'gpa': c['jd'],
            'teacher': c['jsxm']
        } for c in res_dict['body']['dataStores']['kccjStore']['rowSet']['primary']]

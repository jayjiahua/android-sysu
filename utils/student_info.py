# -*- coding: utf-8 -*-
#!/usr/bin/env python

def get_student_info(request_session):
    request_head = {
        'Accept': '*/*',
        'ajaxRequest': 'true',
        'render': 'unieap',
        '__clientType': 'unieap',
        'workitemid': 'null',
        'resourceid': 'null',
        'Content-Type': 'multipart/form-data',
        'Referer': 'http://uems.sysu.edu.cn/jwxt/forward.action?path=/sysu/xj/grwh/grwh_modify',
        'Accept-Language': 'zh-Hans-CN, zh-Hans; q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.3; WOW64; Trident/7.0; .NET4.0E; .NET4.0C; .NET CLR 3.5.30729; .NET CLR 2.0.50727; .NET CLR 3.0.30729)',
        'Host': 'uems.sysu.edu.cn',
        'Content-Length': 291,
        'Connection': 'Keep-Alive',
        'Pragma': 'no-cache'
    }

    request_body = {
        "header": {
            "code": -100,
            "message": {
                "title": "",
                "detail": ""}
        },
        "body": {
            "dataStores": {
                "xsxxStore": {
                    "rowSet": {
                        "primary": [],
                        "filter":[],
                        "delete":[]
                    },
                    "name": "xsxxStore",
                    "pageNumber": 1,
                    "pageSize": 10,
                    "recordCount": 0,
                    "rowSetName": "pojo_com.neusoft.education.sysu.xj.grwh.model.Xsgrwhxx"
                }
            },
            "parameters": {
                "args": [""]
            }
        }
    }


    res = request_session.post("http://uems.sysu.edu.cn/jwxt/WhzdAction/WhzdAction.action?method=getGrwhxxList",
                           headers=request_head, json=request_body)
    res_dict = eval(res.content, type('Dummy', (dict,), dict(__getitem__=lambda s,n:n))())
    student_info_all = res_dict['body']['dataStores']['xsxxStore']['rowSet']['primary'][0]
    student_info = {
        "student_id": student_info_all["xh"],
        "name": student_info_all["xm"],
        "sex": student_info_all["xbm"],
        "class_name": student_info_all["bjmc"],
        "school": student_info_all["xymc"],
        "major": student_info_all["zyfxmc"],
        "grade": student_info_all["njmc"]
    }
    return student_info

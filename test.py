"""
@FILE_NAME : test
-*- coding : utf-8 -*-
@Author : Zhaokugua
@Time : 2022/1/1 12:47
"""
import requests

from pytyut import Pytyut


if __name__ == "__main__":
    Pytyut.node_link = 'https://jxgl20201105.tyutmate.cn/'
    Pytyut.req_headers_add = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63030532)',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Referer': 'https://helper.tyutmate.cn/tyut/index.html?random=fuckyo',
    }
    zkg = Pytyut('学号', '教务系统的密码')
    zkg.login(debug=True)
    class_schedule = zkg.get_class_schedule()
    print('喵')


"""
@FILE_NAME : test
-*- coding : utf-8 -*-
@Author : Zhaokugua
@Time : 2022/1/1 12:47
"""
import requests

from pytyut import Pytyut


if __name__ == "__main__":
    # 建议初始化时自己自定义好节点或者使用自动节点选择（校园网结点权重优先）
    Pytyut.node_link = Pytyut.auto_node_chose(debug=True)
    zkg = Pytyut('学号', '教务系统的密码')
    zkg.login(debug=True)

    print('喵')


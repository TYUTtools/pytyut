"""
@FILE_NAME : pytyut
-*- coding : utf-8 -*-
@Author : Zhaokugua
@Time : 2022/1/3 0:23
@Version V0.3 beta
"""
import requests
import re
import json


class Pytyut:
    default_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/90.0.4430.212 Safari/537.36 Edg/90.0.818.66',
    }
    req_headers_add = {}  # 设置全局请求头（用于特殊节点的请求验证）
    node_link = None   # 设置默认节点
    login_pub_key = '''-----BEGIN PUBLIC KEY-----
    MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCoZG+2JfvUXe2P19IJfjH+iLmp
    VSBX7ErSKnN2rx40EekJ4HEmQpa+vZ76PkHa+5b8L5eTHmT4gFVSukaqwoDjVAVR
    TufRBzy0ghfFUMfOZ8WluH42luJlEtbv9/dMqixikUrd3H7llf79QIb3gRhIIZT8
    TcpN6LUbX8noVcBKuwIDAQAB
    -----END PUBLIC KEY-----
        '''

    def __init__(self, uid, pwd):
        """
        初始化用户信息
        :param uid: 学号
        :param pwd: 教务系统的密码
        """
        self.uid = uid
        self.__pwd = pwd
        self.session = None   # 初始化session

    def login(self, debug=False):
        """
        :param debug:是否打印调试信息
        登录教务系统
        :return:成功返回真实姓名 失败返回None
        """
        if not self.node_link:
            print('未选择登录节点！') if debug else ''
            return None
        self.session = requests.Session()
        login_url = self.node_link + 'Login/CheckLogin'
        # 创建会话，获取ASP.NET_SessionId的Cookies
        self.default_headers.update(self.req_headers_add)
        self.session.get(self.node_link, headers=self.default_headers)
        login_data = {
            'username': self.__RSA_uid(self.uid),
            'password': self.__pwd,
            'code': '',
            'isautologin': 0,
        }
        headers_check_login = {
            'Accept': 'application / json, text / javascript, * / *; q = 0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36 Edg/91.0.864.48',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': self.node_link,
            'Referer': self.node_link,
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        }
        login_res = self.session.post(url=login_url, data=login_data, headers=headers_check_login)
        if '登录成功' in login_res.text:
            print(login_res.json()['message'][:-1], end='：') if debug else ''
            home_url = self.node_link + '/Home/Default'
            home_res = self.session.get(url=home_url, headers=self.default_headers).text
            html = home_res.replace(' ', '').replace('\n', '').replace('\t', '').replace('\r', '')
            name_pattern = '<small>Welcome,</small>([^*]*)</span><ic'
            real_name = re.search(name_pattern, html, ).group(1)
            print(real_name) if debug else ''
            return real_name
        else:
            print('登录失败：', end='') if debug else ''
            print(login_res.json()['message']) if debug else ''
            return None

    @classmethod
    def auto_node_chose(cls, debug=False):
        """
        自动确认登录节点
        :param debug:是否打印调试信息
        :return:登录节点的链接，如：http://jxgl1.tyut.edu.cn/
        """
        test_url = 'http://jxgl1.tyut.edu.cn/'
        print("正在测试最快速的连接，请稍后...")if debug else ''
        try:
            print("节点1...", end='')if debug else ''
            req = requests.get(test_url, timeout=3, headers=cls.default_headers)
            print(req.elapsed.microseconds/1000 + req.elapsed.seconds*100, 'ms')if debug else ''
        except:
            print('超时')if debug else ''
            print("节点2...", end='')if debug else ''
            test_url = 'http://jxgl2.tyut.edu.cn/'
            try:
                req = requests.get(test_url, timeout=3, headers=cls.default_headers)
                print(req.elapsed.microseconds/1000 + req.elapsed.seconds*100, 'ms')if debug else ''
            except:
                print('超时')if debug else ''
                print("节点3...", end='')if debug else ''
                test_url = 'https://jxgl20201105.tyutmate.cn/'
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63030532)',
                    'Sec-Fetch-Site': 'same-site',
                    'Sec-Fetch-Mode': 'navigate',
                    'Sec-Fetch-User': '?1',
                    'Sec-Fetch-Dest': 'document',
                    'Referer': 'https://helper.tyutmate.cn/tyut/index.html?random=fuckyo',
                }

                try:
                    req = requests.get(test_url, timeout=10, headers=headers)
                    if req.status_code != 200:
                        print("服务器错误！请避免高峰期访问！", req.status_code)
                        return None
                    print(req.elapsed.microseconds / 1000 + req.elapsed.seconds * 1000, 'ms')if debug else ''
                    cls.req_headers_add = headers
                except:
                    print("所有节点均无响应，请检查网络！")
                    return None

        print("选择到节点：", test_url)if debug else ''
        return test_url

    @classmethod
    # RSA 公钥加密，用于登录教务系统处理用户名信息
    def __RSA_uid(cls, uid):
        import base64
        # 这里有可能出现导包导不进去的问题，把site-packages里面的crypto文件夹改为大写Crypto即可
        # 需要安装pycryptodome
        from Crypto.PublicKey import RSA
        from Crypto.Cipher import PKCS1_v1_5
        # 公钥在页面里面
        pub_key = cls.login_pub_key
        rsakey = RSA.importKey(pub_key)
        cipher = PKCS1_v1_5.new(rsakey)
        cipher_text = base64.b64encode(cipher.encrypt(uid.encode(encoding='utf-8')))
        value = cipher_text.decode('utf-8')
        return value

    def get_class_schedule(self):
        """
        获取自己的课表信息
        :return: 返回课表json信息
        """
        if not self.session:
            print('未登录')
            return None
        res = self.session.post(self.node_link + 'Tresources/A1Xskb/GetXsKb', headers=self.default_headers)
        if '出错' in res.text or '教学管理服务平台(S)' in res.text:
            print('登录失效！')
            return None
        return res.json()

    def get_class_scores(self):
        """
        获取课程成绩
        :return: 返回课程成绩json信息
        """
        if not self.session:
            print('未登录')
            return None
        req_data = {
            'order': 'zxjxjhh desc,kch',
        }
        req_url = self.node_link + 'Tschedule/C6Cjgl/GetKccjResult'
        res = self.session.post(req_url, headers=self.default_headers, data=req_data)
        if '出错' in res.text or '教学管理服务平台(S)' in res.text:
            print('登录失效！')
            return None
        # 正则匹配学年学期，按照学年学期分开每一个片段
        time_list = re.findall(r'\d{4}-\d{4}学年[\u4e00-\u9fa5]季', res.text)
        score_dict_list = []
        for i in range(len(time_list)):
            if i < len(time_list) - 1:
                html_part = res.text[res.text.find(time_list[i]): res.text.find(time_list[i + 1])]
            else:
                html_part = res.text[res.text.find(time_list[i]):]
            info_list = re.findall(r'tyle="vertical-align:middle; ">([^^]*?)</td>', html_part)
            for j in range(len(info_list) // 9):
                score_dict = {
                    'Xnxq': time_list[i],
                    'Kch': info_list[9 * j],
                    'Kxh': info_list[9 * j + 1],
                    'Kcm': info_list[9 * j + 2],
                    'Kcm_en': info_list[9 * j + 3],
                    'Xf': info_list[9 * j + 4],
                    'Kcsx': info_list[9 * j + 5],
                    'Kssj': info_list[9 * j + 6],
                    'Cj': info_list[9 * j + 7],
                    'Failed_reason': info_list[9 * j + 8],
                }
                score_dict_list.append(score_dict)
        return score_dict_list

    def get_test_info(self, xnxq, bydesk=False):
        """
        获取考试安排信息
        byDesk=True时，xnxq可以传任意参数，不受影响。
        :param bydesk: 使用教务系统主页的简化接口
        :param xnxq: 学年学期，如'2020-2021-1-1'表示2020-2021学年第一学期，同理'2020-2021-2-1'为第二学期
        :return:返回考试安排的json信息
        """
        if not self.session:
            print('未登录')
            return None
        if bydesk:
            req_url = self.node_link + 'Tschedule/C5KwBkks/GetKsxxByDesk'
            data = {
                'pagination[limit]': 15,
                'pagination[offset]': 1,
                'pagination[sort]': 'ksrq',
                'pagination[order]': 'asc',
                'pagination[conditionJson]': '{}',
            }
            res = self.session.post(req_url, headers=self.default_headers, data=data)
            if '出错' in res.text or '教学管理服务平台(S)' in res.text:
                print('登录失效！')
                return None
            html_text = json.loads(res.text)["rpath"]["m_StringValue"]
            html_text = html_text.replace('<font style="color: #ff0000">', '').replace('</font>', '')
            param = '''<tr><td height='20%' width='10%' style="vertical-align:middle; ">([^<]*?)</td><td height='20%' width='25%' style="vertical-align:middle; ">([^<]*?)</td><td height='20%' width='37%' style="vertical-align:middle; ">([^<]*?)</td> <td height='20%' width='30%' style="vertical-align:middle; ">([^<]*?)</td></tr>'''
            info_list = re.findall(param, html_text)
            return info_list

        req_url = self.node_link + 'Tschedule/C5KwBkks/GetKsxxByXhListPage'
        data = {
            'limit': 30,
            'offset': 0,
            'sort': 'ksrq',
            'order': 'desc',
            'conditionJson': '{"zxjxjhh":"' + xnxq + '"}'
        }
        res = self.session.post(req_url, headers=self.default_headers, data=data)
        if '出错' in res.text or '教学管理服务平台(S)' in res.text:
            print('登录失效！')
            return None
        return res.json()


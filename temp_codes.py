"""
@FILE_NAME : temp_codes
-*- coding : utf-8 -*-
@Author : Zhaokugua
@Time : 2022/1/27 22:44
"""
# 评教这部分过于复杂，分为四个请求，暂时不考虑（未来可能考虑实例化一个评教对象简化操作）
    def get_pingjiao_list(self):
        """
        获取所有评教人的详情
        :return json:
        """
        if not self.session:
            print('未登录')
            return None
        req_url = self.node_link + 'Tevaluation/CJxpgxs/GetPjrsjPageListJson'
        data = {
            'limit': 50,
            'offset': 0,
            'sort': 'kch,kxh',
            'order': 'asc',
            'conditionJson': '{}',
        }
        res = self.session.post(req_url, headers=self.default_headers, data=data)
        if '出错' in res.text or '教学管理服务平台(S)' in res.text:
            print('登录失效！')
            return None
        return res.json()

    def get_pingjiao_questions(self, kch, kxh, sjdm, bpr):
        """
        :param kch: string 课程号
        :param kxh: string 课序号
        :param sjdm: sjdm 试卷代码上面获取列表的Sjdm
        :param bpr: bpr 被评人
        :return:
        """
        if not self.session:
            print('未登录')
            return None
        url1 = self.node_link + f'Tevaluation/CJxpgxs/JxpgXssjTreeIndex?kch={kch}&kxh={kxh}&sjdm={sjdm}&bpr={bpr}'
        res1 = self.session.get(url1, headers=self.default_headers)
        req_url = self.node_link + 'Tevaluation/CJxpgxs/GetTreeJson'
        data = {
            'sjdm': sjdm,
        }
        res = self.session.post(req_url, headers=self.default_headers, data=data)
        if '出错' in res.text or '教学管理服务平台(S)' in res.text:
            print('登录失效！')
            return None
        return res.json()

    def get_pingjiao_question_info(self, kch, kxh, sjdm, bpr, stdm, dadm=''):
        """
        :param stdm: 试题代码
        :param dadm: 答案代码（一般为空）
        :param kch: string 课程号
        :param kxh: string 课序号
        :param sjdm: sjdm 上面获取列表的Sjdm
        :param bpr: bpr 被评人
        :return: string 试题的html页面
        """
        if not self.session:
            print('未登录')
            return None
        req_url = self.node_link + 'Tevaluation/CJxpgxs/GetSttb'
        data = {
            'queryJson': '{' + f'"sjdm":"{sjdm}","stdm":"{stdm}","kch":"{kch}","kxh":"{kxh}","bpr":"{bpr}","dadm":"{dadm}"' + '}'
        }
        res = self.session.post(req_url, headers=self.default_headers, data=data)
        if '出错' in res.text or '教学管理服务平台(S)' in res.text:
            print('登录失效！')
            return None
        return res.text
"""
提交评教评价：
POST Tevaluation/CJxpgxs/XssjdaForm
data:
list[0][Sjdm]: 12
list[0][Stdm]: 111
list[0][Stmc]: 第7题：教师对课程目标和任务要求所做的说明，对你学习和理解这门课程作用：
list[0][Stlbdm]: 01
list[0][Dadm]: 01
list[0][Kch]: 00006665
list[0][Kxh]: 33
list[0][Bpr]: 104819
list[1][Sjdm]: 12
list[1][Stdm]: 112
list[1][Stmc]: 第1题：教师教学设计，教学内容和教学方法对激发你学习兴趣，改善学习效果作用：
list[1][Stlbdm]: 01
list[1][Dadm]: 01
list[1][Kch]: 00006665
list[1][Kxh]: 33
list[1][Bpr]: 104819
list[2][Sjdm]: 12
list[2][Stdm]: 113
list[2][Stmc]: 第2题：教师营造的课前课堂课后学习环境，对引导学生独立思考探究发挥的作用：
list[2][Stlbdm]: 01
list[2][Dadm]: 01
list[2][Kch]: 00006665
list[2][Kxh]: 33
list[2][Bpr]: 104819
list[3][Sjdm]: 12
list[3][Stdm]: 114
list[3][Stmc]: 第3题：该课程对提升你的专业能力或认知水平，提高分析和解决实际问题的能力发挥的作用
list[3][Stlbdm]: 01
list[3][Dadm]: 01
list[3][Kch]: 00006665
list[3][Kxh]: 33
list[3][Bpr]: 104819
list[4][Sjdm]: 12
list[4][Stdm]: 115
list[4][Stmc]: 第8题：教师提供的答疑和作业批改反馈对你学习课程的帮助？
list[4][Stlbdm]: 01
list[4][Dadm]: 01
list[4][Kch]: 00006665
list[4][Kxh]: 33
list[4][Bpr]: 104819
list[5][Sjdm]: 12
list[5][Stdm]: 116
list[5][Stmc]: 第4题：你对教师的上课时间遵守，备课情况，表达、板书规范等方面教学能力和态度的满意度：
list[5][Stlbdm]: 01
list[5][Dadm]: 01
list[5][Kch]: 00006665
list[5][Kxh]: 33
list[5][Bpr]: 104819
list[6][Sjdm]: 12
list[6][Stdm]: 117
list[6][Stmc]: 第9题：你认为该教师对该门课程学习要求严格程度是
list[6][Stlbdm]: 01
list[6][Dadm]: 02
list[6][Kch]: 00006665
list[6][Kxh]: 33
list[6][Bpr]: 104819
list[7][Sjdm]: 12
list[7][Stdm]: 118
list[7][Stmc]: 第11题：你对于该门课程教学在体现前沿成果，有新意，学习有难度和挑战度方面的评价是
list[7][Stlbdm]: 01
list[7][Dadm]: 02
list[7][Kch]: 00006665
list[7][Kxh]: 33
list[7][Bpr]: 104819
list[8][Sjdm]: 12
list[8][Stdm]: 119
list[8][Stmc]: 第10题：讲课教师有哪些长处？有何改进之处？
list[8][Dadm]: 老师特别好
list[8][Stlbdm]: 02
list[8][Kch]: 00006665
list[8][Kxh]: 33
list[8][Bpr]: 104819
list[9][Sjdm]: 12
list[9][Stdm]: 120
list[9][Stmc]: 第5题：你对教师的总评分（请根据以上评价，对教师按照百分制给出评分）：
list[9][Dadm]: 100
list[9][Stlbdm]: 03
list[9][Kch]: 00006665
list[9][Kxh]: 33
list[9][Bpr]: 104819
list[10][Sjdm]: 12
list[10][Stdm]: 121
list[10][Stmc]: 第6题：主观评价
list[10][Dadm]: 老师讲课幽默风趣，课程质量也很高
list[10][Stlbdm]: 02
list[10][Kch]: 00006665
list[10][Kxh]: 33
list[10][Bpr]: 104819
__RequestVerificationToken: 1nGq5PWsw_m5TJcPVW-8WllGmaI1PIuzkKWV_-m4shk1OrABGCkdTeCYlfkm4hfKkRUYuzZ5S6evkgqEALI9Dzt-2XP8hhaokmFjVLeUIcA1
"""
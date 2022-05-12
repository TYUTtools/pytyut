# pytyut

### 介绍
使用python与太原理工相连！

现在已经有很多基于此开发的实用工具！

[太理全校课程表爬取<br>https://gitee.com/jixiaob/TyutClassScheduleCrawler](https://gitee.com/jixiaob/TyutClassScheduleCrawler)

[太理教务系统选课脚本<br>https://gitee.com/jixiaob/tyut_class_choose](https://gitee.com/jixiaob/tyut_class_choose)


### 外部包引用
使用前请确保已经安装了以下第三方包：
>pip install requests
><br>
> pip install pycryptodome

### 目前功能概况
| 组件                                     | 版本        | 描述                |
|----------------------------------------|-----------|-------------------|
| Pytyut.node_link                       | 2022/1/2  | 自定义登录节点           |
| Pytyut.req_headers_add                 | 2022/1/2  | 自定义登录header       |
| Pytyut.login_pub_key                   | 2022/1/2  | 自定义登录公钥（公钥被更改时使用） |
| self.login()                           | 2022/1/2  | 教务系统的基础登录功能       |
| self.get_test_info()                   | 2022/1/2  | 考试安排信息查询          |
| self.get_class_scores()                | 2022/1/2  | 成绩查询              |
| self.get_class_schedule()              | 2022/1/2  | 查看自己的课表信息         |
| self.get_class_schedule_by_bjh()       | 2022/2/8  | 查看任意专业班级的课表       |
| self.get_major_class_tree()            | 2022/2/8  | 获取所有学院专业班级        |
| self.get_my_info()                     | 2022/2/10 | 查看个人信息            |
| self.get_xq_page_list()                | 2022/2/13 | 获取选课科目列表          |
| self.get_xk_kc_list()                  | 2022/2/13 | 获取科目中可选课程列表       |
| self.get_chosen_course_list()          | 2022/2/23 | 获取已选择的课程列表        |
| self.choose_course()                   | 2022/2/23 | 提交选课请求表单          |
| self.remove_course()                   | 2022/2/23 | 提交退课请求表单          |
| self.get_total_grades_result()         | 2022/5/12 | 总成绩 绩点 排名查询       |
| self.session.get() self.session.post() | 2022/1/2  | 自定义请求             |

要填的坑：
- [ ] 学生评教
- [ ] ……

### [wiki文档](https://gitee.com/jixiaob/pytyut/wikis/%E5%BC%80%E5%A7%8B/%E7%AE%80%E4%BB%8B)
具体的使用方法，请查看我们的[wiki文档](https://gitee.com/jixiaob/pytyut/wikis/%E5%BC%80%E5%A7%8B/%E7%AE%80%E4%BB%8B)。

### 快速开始：
1. 将pytyut.py下载下来
2. 引入Pytyut类：
```python
from pytyut import Pytyut
```
3. 设置连接节点
```python
Pytyut.node_link = 'http://jxgl1.tyut.edu.cn/'
```
也可以自动测试选择最佳节点
```python
Pytyut.node_link = Pytyut.auto_node_chose(debug=True)
```
4. 创建用户对象并登录
```python
# 学号里面填学号，202000xxxx之类的，密码是教务系统的密码
zkg = Pytyut('学号', '教务系统的密码')
zkg.login(debug=True)
```
登录之后就可以使用对象里面的方法了。
比如：
```python
class_schedule = zkg.get_class_schedule()
```
这样就能获取到课程信息的json数据了。



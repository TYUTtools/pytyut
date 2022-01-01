# pytyut

### 介绍
使用python与太原理工相连！

### 外部包引用
使用前请确保已经安装了以下第三方包：
>pip install requests
><br>
> pip install pycryptodome

### 目前功能概况
- [x] 教务系统的基础登录功能
- [x] 自定义登录节点
- [x] 自定义登录header
- [x] 自定义登录公钥（公钥被更改时使用）
- [x] debug模式（可选是否打印调试信息）
- [ ] 教务系统选课
- [ ] 成绩查询
- [ ] 绩点查询
- [ ] 学生评教
- [x] 查看课表信息
- [ ] 查看全校课表
- [ ] 自定义请求
- [ ] ……

### 使用方法：
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
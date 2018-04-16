##### 安装以下库
```python
pip install selenium openpyxl lxml pandas beautifulsoup4 logging pickle configparser
```

注意：windows下，phantomjs需要手动安装

##### 打开huya.xlsx，填写账号密码
现版本只支持账号/邮箱/YY号/手机号码登录

##### 无头模式：即不打开浏览器在后台运行
```python
python main.py -ph
```

##### 谷歌浏览器模式: 用于开发与维护
```python
python main.py -ch
```

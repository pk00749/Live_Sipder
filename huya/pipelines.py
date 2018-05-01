# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pickle
from selenium import webdriver


class HuyaPipeline(object):

    def __init__(self):
        self.driver = self.start_chrome()

    def process_item(self, item, spider):
        self.is_login(item.get('room_url'))
        return item

    def open_spider(self, spider):
        self.driver.get("https://www.huya.com/g/lol")
        self.set_cookie()
        self.driver.refresh()

    def close_spider(self, spider):
        # self.driver.close()
        pass

    def is_login(self, room_url):
    #     # login_name = driver.find_element_by_xpath("//*[@id='login-username']").text
    #     # print(response.xpath('//span[@id="login-username"]/@title').extract()[0])
        if self.driver.find_element_by_xpath("//*[@id='login-username']").text == "":
            print('Need to login')
        else:
            print("NO need to login")
            self.driver.get(room_url)
            # print('URL opened: ' + room_url)

    def start_chrome(self):
        service_args=[]
        service_args.append('--load-image=no')
        service_args.append('--disk-cache=yes')
        service_args.append('--ignore-ssl-errors=true')
        driver = webdriver.PhantomJS() # service_args=service_args
        driver.maximize_window()
        driver.implicitly_wait(30)  # 隐式等待
        return driver

    def set_cookie(self):
        try:
            cookies = pickle.load(open("cookies.pkl", "rb"))
            for cookie in cookies:
                cookie_dict = {
                    "domain": ".huya.com",  # 火狐浏览器不用填写，谷歌要需要
                    'name': cookie.get('name'),
                    'value': cookie.get('value'),
                    "expires": "",
                    'path': '/',
                    'httpOnly': False,
                    'HostOnly': False,
                    'Secure': False}
                self.driver.add_cookie(cookie_dict)
        except Exception as e:
            print(e)
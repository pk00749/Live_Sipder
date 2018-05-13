# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pickle, time, os, json
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class HuyaPipeline(object):

    def __init__(self):
        self.driver = self.start_chrome()
        self.json = self.load_json()

    def open_spider(self, spider):
        print('open_spider')
        self.driver.get("https://www.huya.com/g/lol")
        if os.path.exists("./cookies/{username}.pkl".format(username=self.json.get('name'))):
            print("cookie existed.")
            self.set_cookie()
            self.driver.refresh()
        else:
            print("cookie don't existed.")
        self.driver.refresh()

    def close_spider(self, spider):
        # self.driver.close()
        pass

    def process_item(self, item, spider):
        print('process_item')
        self.is_login(item.get('room_url'))
        return item

    def is_login(self, room_url):
    #     # login_name = driver.find_element_by_xpath("//*[@id='login-username']").text
    #     # print(response.xpath('//span[@id="login-username"]/@title').extract()[0])
        if self.driver.find_element_by_xpath("//*[@id='login-username']").text == "": #//*[@id="login-username"]
            print('Need to login')
            self.login()
            self.save_cookie()
        else:
            print("NO need to login")
            self.driver.get(room_url)
            self.send_advertisement()
            # print('URL opened: ' + room_url)

    def start_chrome(self):
        service_args=[]
        service_args.append('--load-image=no')
        service_args.append('--disk-cache=yes')
        service_args.append('--ignore-ssl-errors=true')
        driver = webdriver.PhantomJS() # service_args=service_args
        driver.maximize_window()
        # chromedriver = "C:\Program Files\Google\Chrome\Application\chromedriver.exe"
        # os.environ["webdriver.chrome.driver"] = chromedriver
        # option = webdriver.ChromeOptions()
        # # option.add_argument('headless') # can't use
        # driver = webdriver.Chrome(chromedriver, chrome_options=option)

        driver.implicitly_wait(30)  # 隐式等待
        return driver

    def load_json(self):
        return pickle.load(open("./json/temp.pkl", "rb"))

    def save_cookie(self):
        """ 保存cookie """
        # 将cookie序列化保存下来
        pickle.dump(self.driver.get_cookies(), open("./cookies/{username}.pkl".format(username=self.json.get('name')), "wb"))
        # with open("./cookies/test.txt", "wb") as file:
        #     file.write(self.driver.get_cookies())
        print('------------------------------------------------')
        print(self.driver.get_cookies())
        # jsoncookie =json.dumps(self.driver.get_cookies())
        # with open("./cookies/test_2.json", "wb") as file_2:
        #     file_2.write(jsoncookie)

    def set_cookie(self):
        print('set_cookie')
        try:
            cookies = pickle.load(open("./cookies/{username}.pkl".format(username=self.json.get('name')), "rb"))
            for cookie in cookies:
                print(cookie)
                print(cookie.get('name'))
                print(cookie.get('value'))
                cookie_dict = {
                    "domain": ".huya.com",  # 火狐浏览器不用填写，谷歌要需要
                    'name': cookie.get('name'),
                    'value': cookie.get('value'),
                    "expires": "",
                    'path': '/',
                    'httpOnly': False,
                    'hostOnly': False,
                    'secure': False}
                self.driver.add_cookie(cookie_dict)
        except Exception as e:
            print(e)

    def login(self):
        driver = self.driver
        __username = self.json.get('name') # '13250219510'#self.username
        __password =  self.json.get('password')#self.password
        title = driver.title
        print(title)

        # self.driver.find_element_by_link_text("登录").click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'nav-login'))).click()
        # self.driver.find_element_by_id('nav-login').click()
        WebDriverWait(driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//*[@id='udbsdk_frm_normal']")))
        # frame = self.driver.find_element_by_xpath("//*[@id='udbsdk_frm_normal']")
        # self.driver.switch_to.frame(frame)
        time.sleep(1)

        ele = self.driver.find_element_by_xpath("//*[@id='m_commonLogin']/div[1]/span/input")
        ele.send_keys(__username)

        ele = self.driver.find_element_by_xpath("//*[@id='m_commonLogin']/div[2]/span/input")
        ele.send_keys(__password)

        time.sleep(1)
        self.driver.find_element_by_xpath("//*[@id='m_commonLogin']/div[5]/a[1]").click()

        print("Login success")
        # time.sleep(2)
        # self.driver.switch_to.default_content()  # switch to main page

    def send_msg(self, msg):
        msg_input = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='pub_msg_input']")))
        # msg_input = self.driver.find_element_by_xpath("//*[@id='pub_msg_input']")
        msg_input.send_keys(msg)
        time.sleep(2)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, 'msg_send_bt'))).click()
        # driver.find_element_by_xpath("//*[@id='msg_send_bt']").click()
        # self.driver.find_element_by_id('msg_send_bt').click()
        # time.sleep(2)

    def send_advertisement(self):
        # send_frequence = self.workbook.read_cell('设置', 'A2')
        # if self.workbook.read_cell('登录', 'D%d' % self.no):
        #     msg_1 = self.workbook.read_cell('登录', 'D%d' % self.no)
        self.send_msg('666')
            # time.sleep(send_frequence)
        print('Message 1 sent!')
            # if self.workbook.read_cell('登录', 'E%d' % self.no):
            #     msg_2 = self.workbook.read_cell('登录', 'E%d' % self.no)
            #     self.send_msg(msg_2)
            #     print('Message 2 sent!')
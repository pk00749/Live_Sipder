import urllib.request
from selenium import webdriver
import time
import os
import pandas as pd
import csv
from module.config import Config
import pickle


class Huya_Sipder:

    def __init__(self):
        self.driver = self.start_chrome()

    def __login_info(self):
        config = Config()
        login = config.get_config_info()
        login_info = config.get_config_info()
        return login_info['username'], login['password']

    def start_chrome(self):
        chromedriver = "C:\Program Files\Google\Chrome\Application\chromedriver.exe"
        os.environ["webdriver.chrome.driver"] = chromedriver
        driver = webdriver.Chrome(chromedriver)
        driver.implicitly_wait(30)  # 隐式等待
        return driver

    def read_csv(self):
        all_urls = []
        reader = csv.reader(open('room_list.csv', encoding='utf-8'))
        for url in reader:
            all_urls.append(url[1])

        total_url = len(all_urls)
        return total_url, all_urls


    def is_login(self):
        url = "http://www.huya.com/a16789"
        self.driver.get(url)
        # html = self.driver.page_source
        # print(html.find("登录"))
        # u, p = self.__login_info()
        # //*[@id="login-username"]
        if self.driver.find_element_by_xpath("//*[@id='login-username']").text == "":
            print('Need to login')
            self.login(url)
        else:
            print("no need to login")

    def logined(self, driver):
        if driver.find_element_by_xpath("//*[@id='login-username']").text == "":
            print('Need to login')
        else:
            print("no need to login")


    def save_cookie(self):
        '''保存cookie'''
        # 将cookie序列化保存下来
        pickle.dump(self.driver.get_cookies(), open("cookies.pkl", "wb"))

    def set_cookie(self):
        '''往浏览器添加cookie'''
        '''利用pickle序列化后的cookie'''
        try:
            cookies = pickle.load(open("cookies.pkl", "rb"))
            for cookie in cookies:
                cookie_dict = {
                    "domain": ".baidu.com",  # 火狐浏览器不用填写，谷歌要需要
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

    def login(self, url):
        # driver = webdriver.PhantomJS()
        # driver.get("http://hotel.qunar.com/")
        driver = self.driver
        # url="http://www.huya.com/a16789"
        __username, __password = self.__login_info()
        driver.get(url)
        driver.implicitly_wait(15)
        title = driver.title
        print(title)

        driver.find_element_by_link_text("登录").click()
        driver.implicitly_wait(15)
        frame = driver.find_element_by_xpath("//*[@id='udbsdk_frm_normal']")
        driver.switch_to.frame(frame)
        time.sleep(3)

        ele = driver.find_element_by_xpath("//*[@id='m_commonLogin']/div[1]/span/input")
        ele.send_keys(__username)

        ele = driver.find_element_by_xpath("//*[@id='m_commonLogin']/div[2]/span/input")
        ele.send_keys(__password)

        time.sleep(2)
        driver.find_element_by_xpath("//*[@id='m_commonLogin']/div[5]/a[1]").click()

        print("Login success")
        # self.logined(driver)
        time.sleep(5)
        driver.switch_to.default_content()  # switch to main page


        msg = driver.find_element_by_xpath("//*[@id='pub_msg_input']")
        msg.send_keys('Hello')
        time.sleep(3)
        # driver.find_element_by_xpath("//*[@id='msg_send_bt']").click()
        driver.find_element_by_id('msg_send_bt').click()
        time.sleep(3)
        msg = driver.find_element_by_xpath("//*[@id='pub_msg_input']")
        return driver

    def send_msg(self):
        # driver = self.open_url(url)
        pass

    def main(self):
        total_url, all_urls = self.read_csv()
        for u in range(1, total_url):
            url = all_urls[u]
            print(url)
            self.login(url)


if __name__ == '__main__':
    huya = Huya_Sipder()
    huya.is_login()

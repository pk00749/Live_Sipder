import urllib.request
from selenium import webdriver
import time
import os
import pandas as pd
import csv
from module.config import Config


class Huya_Sipder:

    def __int__(self):
        self.driver = self.start_chrome()

    def login_info(self):
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

    def open_url(self, url):
        # driver = webdriver.PhantomJS()
        # driver.get("http://hotel.qunar.com/")
        driver = self.start_chrome()
        # url="http://www.huya.com/a16789"
        driver.get(url)
        driver.implicitly_wait(15)
        data = driver.title
        print(data)

        return driver

    def send_msg(self, url):
        username, password = self.login_info()
        driver = self.open_url(url)
        driver.find_element_by_link_text("登录").click()
        driver.implicitly_wait(15)
        frame = driver.find_element_by_xpath("//*[@id='udbsdk_frm_normal']")
        driver.switch_to.frame(frame)
        time.sleep(3)
        ele = driver.find_element_by_xpath("//*[@id='m_commonLogin']/div[1]/span/input")
        ele.send_keys(username)

        ele = driver.find_element_by_xpath("//*[@id='m_commonLogin']/div[2]/span/input")
        ele.send_keys(password)

        time.sleep(2)
        driver.find_element_by_xpath("//*[@id='m_commonLogin']/div[5]/a[1]").click()
        print("Login success")
        time.sleep(5)
        driver.switch_to.default_content() # switch to main page
        msg = driver.find_element_by_xpath("//*[@id='pub_msg_input']")
        msg.send_keys('Hello')
        time.sleep(3)
        # driver.find_element_by_xpath("//*[@id='msg_send_bt']").click()
        driver.find_element_by_id('msg_send_bt').click()
        time.sleep(3)
        msg = driver.find_element_by_xpath("//*[@id='pub_msg_input']")

    def main(self):
        total_url, all_urls = self.read_csv()
        for u in range(1, total_url):
            url = all_urls[u]
            print(url)
            self.send_msg(url)


if __name__ == '__main__':
    huya = Huya_Sipder()
    huya.main()

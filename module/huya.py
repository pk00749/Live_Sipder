import urllib.request
from selenium import webdriver
import time
import os
import csv
from module.config import Config
import pickle
from module.admin_excel import AdminWorkbook


class Spider:

    def __init__(self, username, password, msg):
        self.driver = self.start_chrome()
        self.username = username
        self.password = password
        self.msg = msg

    def start_chrome(self):
        chromedriver = "C:\Program Files\Google\Chrome\Application\chromedriver.exe"
        os.environ["webdriver.chrome.driver"] = chromedriver
        driver = webdriver.Chrome(chromedriver)
        driver.implicitly_wait(30)  # 隐式等待
        return driver

    def read_csv(self):
        all_urls = []
        reader = csv.reader(open('../room_list.csv', encoding='utf-8'))
        for url in reader:
            all_urls.append(url[1])

        total_url = len(all_urls)
        return total_url, all_urls

    def save_cookie(self):
        """ 保存cookie """
        # 将cookie序列化保存下来
        pickle.dump(self.driver.get_cookies(), open("cookies.pkl", "wb"))

    def set_cookie(self):
        """ 往浏览器添加cookie 利用pickle序列化后的cookie """

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

    def login(self):
        # driver = webdriver.PhantomJS()
        # driver.get("http://hotel.qunar.com/")
        driver = self.driver
        __username = self.username
        __password = self.password
        # driver.implicitly_wait(15)
        title = driver.title
        print(title)

        self.driver.find_element_by_link_text("登录").click()
        self.driver.implicitly_wait(15)
        frame = self.driver.find_element_by_xpath("//*[@id='udbsdk_frm_normal']")
        self.driver.switch_to.frame(frame)
        time.sleep(3)

        ele = self.driver.find_element_by_xpath("//*[@id='m_commonLogin']/div[1]/span/input")
        ele.send_keys(__username)

        ele = self.driver.find_element_by_xpath("//*[@id='m_commonLogin']/div[2]/span/input")
        ele.send_keys(__password)

        time.sleep(1)
        self.driver.find_element_by_xpath("//*[@id='m_commonLogin']/div[5]/a[1]").click()

        print("Login success")
        time.sleep(3)
        self.driver.switch_to.default_content()  # switch to main page

    def send_msg(self):
        msg = self.driver.find_element_by_xpath("//*[@id='pub_msg_input']")
        msg.send_keys(self.msg)
        time.sleep(3)
        # driver.find_element_by_xpath("//*[@id='msg_send_bt']").click()
        self.driver.find_element_by_id('msg_send_bt').click()
        time.sleep(3)

    def main(self):
        total_url, all_urls = self.read_csv()
        for u in range(1, total_url):
            url = all_urls[u]
            print(url)
            self.driver.get(url)
            time.sleep(3)
            if self.driver.find_element_by_xpath("//*[@id='login-username']").text == "":
                print('Need to login')
                self.login()
                self.save_cookie()
                self.send_msg()
            else:
                print("No need to login")
                self.send_msg()


def huya_spider(file):
    workbook = AdminWorkbook(file)
    workbook.load_workbook()

    for i in range(1,2):
        username = workbook.read_cell('登录', 'A%d'% (i + 1))
        password = workbook.read_cell('登录', 'B%d' % (i + 1))
        msg = workbook.read_cell('登录', 'D%d' % (i + 1))
        spider = Spider(username, password, msg)
        spider.main()

if __name__ == '__main__':
    huya_spider('../huya.xlsx')

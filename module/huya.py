import urllib.request
from selenium import webdriver
import time
import os
import csv
import pickle
from module.admin_excel import AdminWorkbook
from module.get_rooms import GetRooms

TOTAL_ADVERTISEMENT = 2


class Spider:

    def __init__(self, file, username, password, no, browser):
        self.driver = self.start_chrome(browser)
        self.username = username
        self.password = password
        self.workbook = AdminWorkbook(file)
        self.no = no

    def start_chrome(self, browser):
        if browser == '-ch':
            chromedriver = "C:\Program Files\Google\Chrome\Application\chromedriver.exe"
            os.environ["webdriver.chrome.driver"] = chromedriver
            driver = webdriver.Chrome(chromedriver)
        else:
            driver = webdriver.PhantomJS()
            driver.maximize_window()
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
        driver = self.driver
        __username = self.username
        __password = self.password
        # driver.implicitly_wait(15)
        title = driver.title
        print(title)

        # self.driver.find_element_by_link_text("登录").click()
        # nav-login
        # //*[@id="nav-login"]
        self.driver.find_element_by_id('nav-login').click()
        # self.driver.find_element_by_class_name('')
        # self.driver.find_element_by_xpath("//*[@id='J_duyaHeaderRight']/div/div[5]/div/div").click()
        # //*[@id="J_duyaHeaderRight"]/div/div[5]/div/div
        # //*[@id="nav-login"]
        
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

    def send_msg(self, msg):
        msg_input = self.driver.find_element_by_xpath("//*[@id='pub_msg_input']")
        msg_input.send_keys(msg)
        time.sleep(3)
        # driver.find_element_by_xpath("//*[@id='msg_send_bt']").click()
        self.driver.find_element_by_id('msg_send_bt').click()
        time.sleep(3)


    def send_advertisement(self):
        send_frequence = self.workbook.read_cell('设置', 'A2')
        if self.workbook.read_cell('登录', 'D%d' % self.no):
            msg_1 = self.workbook.read_cell('登录', 'D%d' % self.no)
            self.send_msg(msg_1)
            time.sleep(send_frequence)
            print('Message 1 sent!')
            if self.workbook.read_cell('登录', 'E%d' % self.no):
                msg_2 = self.workbook.read_cell('登录', 'E%d' % self.no)
                self.send_msg(msg_2)
                print('Message 2 sent!')

    def close_driver(self):
        self.driver.close()

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
                self.send_advertisement()
            else:
                print("No need to login")
                self.send_advertisement()


def huya_spider(file, browser):
    workbook = AdminWorkbook(file)
    workbook.load_workbook()
    get_rooms = GetRooms(file)

    for i in range(1, workbook.get_max_row('登录') + 1):
        no = i + 1
        get_rooms.get_room_list(no)
        username = workbook.read_cell('登录', 'A%d' % no)
        if username:
            password = workbook.read_cell('登录', 'B%d' % no)
            if password:
                spider = Spider(file, username, password, no, browser)
                spider.main()
                spider.close_driver()
            else:
                print("No Password!!!")
        else:
            print("No User Name!!!")


if __name__ == '__main__':
    huya_spider('../huya.xlsx', '-ch')
    # t = Spider('../huya.xlsx','13250219510','81302137hy',1)
    # print(t.main())
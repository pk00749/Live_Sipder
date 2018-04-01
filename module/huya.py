from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import os
import pickle
from module.admin_excel import AdminWorkbook
from module.get_rooms import GetRooms


class Spider:

    def __init__(self, file, username, password, no, browser):
        self.driver = self.start_chrome(browser)
        self.username = username
        self.password = password
        self.workbook = AdminWorkbook(file)
        self.topic = ''
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

    def read_csv(self, no):
        topic = self.workbook.read_cell('登录', 'C%d' % no)
        return self.workbook.get_max_row(topic)
        # all_urls = []
        # reader = csv.reader(open('../room_list.csv', encoding='utf-8'))
        # for url in reader:
        #     all_urls.append(url[1])
        #
        # total_url = len(all_urls)
        # return total_url, all_urls

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
        time.sleep(2)
        self.driver.switch_to.default_content()  # switch to main page

    def send_msg(self, msg):
        msg_input = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='pub_msg_input']")))
        # msg_input = self.driver.find_element_by_xpath("//*[@id='pub_msg_input']")
        msg_input.send_keys(msg)
        time.sleep(3)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, 'msg_send_bt'))).click()
        # driver.find_element_by_xpath("//*[@id='msg_send_bt']").click()
        # self.driver.find_element_by_id('msg_send_bt').click()
        time.sleep(2)

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

    def main(self, no):
        # total_url, all_urls = self.read_csv()
        topic = self.workbook.read_cell('登录', 'C%d' % no)
        total_url =  self.workbook.get_max_row(topic)
        for u in range(1, total_url):
            # url = all_urls[u]
            url = self.workbook.read_cell(topic,'B%d' % u)
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
    room_list = GetRooms(file)

    for i in range(1, workbook.get_max_row('登录') + 1):
        no = i + 1
        # room_list.get_all_rooms_list(no)
        username = workbook.read_cell('登录', 'A%d' % no)
        if username:
            password = workbook.read_cell('登录', 'B%d' % no)
            if password:
                spider = Spider(file, username, password, no, browser)
                spider.main(no)
                spider.close_driver()
            else:
                print("No Password!!!")
        else:
            print("No User Name!!!")


if __name__ == '__main__':
    huya_spider('../huya.xlsx', '-ch')
    # t = Spider('../huya.xlsx','13250219510','81302137hy',1)
    # print(t.main())

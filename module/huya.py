from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import os
import pickle
from module.admin_excel import AdminWorkbook
from module.get_rooms import GetRooms
import logging, json


class Spider:

    def __init__(self, username, password, no, browser):
        self.driver = self.start_chrome(browser)
        self.username = username
        self.password = password
        # self.workbook = AdminWorkbook(file)
        self.topic = ''
        self.no = no
        self.logger = logging.getLogger()
        self.total_rooms = 0
        self.room_base_url = 'https://www.huya.com/'

    def start_chrome(self, browser):
        print("start_chrome")
        if browser == '-ch':
            chromedriver = "C:\Program Files\Google\Chrome\Application\chromedriver.exe"
            os.environ["webdriver.chrome.driver"] = chromedriver
            # driver = webdriver.Chrome(chromedriver)
            option = webdriver.ChromeOptions()
            # option.add_argument('headless')

            driver = webdriver.Chrome(chromedriver, chrome_options=option)
        else:
            driver = webdriver.PhantomJS(service_args=['--disk-cache=yes'])
            driver.maximize_window()
        driver.implicitly_wait(30)  # 隐式等待
        return driver

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

    def close_driver(self):
        self.driver.close()


    def get_topic_url(self):
        print('get_topic_url')
        topic = '绝地求生' # self.workbook.read_cell('登录', 'C%d' % self.no)
        self.driver.get('https://www.huya.com/g/')
        all_topics = self.driver.find_elements_by_xpath('//ul[@class="game-list clearfix"]/li')
        print(all_topics)
        self.logger.info('Topic: ' + topic)
        for each_topic in all_topics:
            if topic == each_topic.find_element_by_xpath('./a/img/@title').text:
                gid = each_topic.find_element_by_xpath('./@gid').extract()[0]
                topic_href = each_topic.find_element_by_xpath('./a/@href').extract()[0]
                self.logger.info('ID: ' + gid)
                self.logger.info("URL of the topic: " + topic_href)
                return gid, topic_href

    def get_page(self, topic_url):
        print('get_page')
        self.logger.info("METHOD - page, visited by %s", topic_url)
        self.driver.get(topic_url)
        total_pages = self.driver.find_elements_by_xpath('//div[@class="list-page"]/@data-pages').extract()[0]
        self.logger.info("Total pages of the topic: " + total_pages)
        return total_pages

    def topic_url_by_page(self, gid, page):
        return 'https://www.huya.com/cache.php?m=LiveList&do=getLiveListByPage&gameId={gid}&tagAll=0&page={page}'.format(
            gid=gid, page=page)

    def get_rooms(self, url):

        print('get_rooms')
        self.logger.info("METHOD - get_topic_url, visited by %s", url)
        self.driver.get(url)
        body = self.driver.page_source
        body_str = body.decode()
        body_json = json.loads(body_str)
        total_rooms_by_page = len(body_json['data']['datas'])
        self.total_rooms += total_rooms_by_page
        for room in range(0, total_rooms_by_page):
            room_id = body_json['data']['datas'][room]['profileRoom']
            room_url = self.room_base_url + room_id
            time.sleep(2)
            yield room_url
        self.logger.info('Total rooms: ' + str(self.total_rooms))

    def main(self):
        print('main')
        gid, url = self.get_topic_url()
        total_pages = self.get_page(url)
        for p in range(1, int(total_pages) + 1):
            url = self.topic_url_by_page(gid, p)
            self.get_rooms(url)

            time.sleep(3)

            if self.driver.find_element_by_xpath("//*[@id='login-username']").text == "":
                print('Need to login')
                self.login()
                self.save_cookie()
                self.send_advertisement()
            else:
                print("No need to login")
                self.send_advertisement()


def huya_spider(browser):
    spider = Spider('13250219510', '81302137hy', 2, browser)
    spider.main()
    spider.close_driver()

if __name__ == '__main__':
    huya_spider('hl')
    # t = Spider('../huya.xlsx','13250219510','81302137hy',1)
    # print(t.main())

import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from module.admin_excel import AdminWorkbook
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.phantomjs.webdriver

# TODO: get number of audiences
# TODO: list title into csv


class GetRooms:
    def __init__(self, file):
        self.workbook = AdminWorkbook(file)
        self.driver = self.start_browser()
        self.total_rooms = 0

    def get_base_url(self):
        base_url = self.workbook.read_cell('设置','B2')
        return base_url

    def start_browser(self):
        driver = webdriver.PhantomJS()
        driver.maximize_window()
        driver.implicitly_wait(30)  # 隐式等待
        return driver

    def get_page_soup(self, url):
        headers = {
            "Host": "www.huya.com",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"
        }
        # 构造好请求对象 将请求提交到服务器 获取的响应就是到首页的html代码
        request = urllib.request.Request(url=url, headers=headers)
        response = urllib.request.urlopen(request)
        page_soup = BeautifulSoup(response.read(), "lxml")
        return page_soup

    def get_all_topics(self):
        self.workbook.load_workbook()
        i = 1

        base_url = self.get_base_url()
        page_soup =self.get_page_soup(base_url)
        topics = page_soup.find("ul", attrs={"class": "game-list clearfix"})
        total_topics = len(topics.find_all('a', target='_blank', href=True))
        print(total_topics)

        for a in topics.find_all('a', target='_blank', href=True):
            print(a['href'])
            self.workbook.write_cell('主题列表', 'B%d' % i, a['href'])
            self.workbook.write_cell('主题列表', 'A%d' % i, a.find('h3', class_='title').text)
            i = i + 1

        self.workbook.save_workbook()

    def get_topic_url(self, no):
        topic = self.workbook.read_cell('登录', 'C%d' % no)
        print(topic)
        max_row = self.workbook.get_max_row('主题列表')
        for row in range(1, max_row+1):
            if self.workbook.read_cell('主题列表', 'A%d' % row) == topic:
                print(self.workbook.read_cell('主题列表', 'B%d' % row))
                self.driver.get(self.workbook.read_cell('主题列表', 'B%d' % row))
                # return self.workbook.read_cell('主题列表', 'B%d' % row)
            else:
                continue

    def get_room_list(self):
        page_soup = BeautifulSoup(self.driver.page_source, 'lxml')
        # page_soup = self.get_page_soup(home)
        live_rooms = page_soup.find("ul", attrs={"class": "live-list clearfix"})
        total_rooms_in_page = len(live_rooms.find_all('a', class_='title new-clickstat', href=True))

        print(total_rooms_in_page)
        self.total_rooms += total_rooms_in_page
        print(self.total_rooms)
        hrefs = []

        for a in live_rooms.find_all('a', class_='title new-clickstat', href=True):
            print(a['href'], a['title'])
            hrefs.append(a['href'])

        df = pd.DataFrame(np.array(hrefs))
        df.to_csv('../room_list.csv')

        # for r in range(self.total_rooms+1, total_rooms)
        # self.workbook.write_cell('房间','A%d' % )

    def get_all_rooms_list(self):
        break_flag = False
        while break_flag != True:
            self.get_room_list()
            print(WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'laypage_next'))))
            if  WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'laypage_next'))):
                WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located((By.CLASS_NAME, 'laypage_next'))).click()
                print('next page')
            else:
                break_flag = True


if __name__ == '__main__':
    t = GetRooms('../huya.xlsx')
    t.get_topic_url(2)
    t.get_all_rooms_list()


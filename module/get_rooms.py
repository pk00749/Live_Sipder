import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from module.admin_excel import AdminWorkbook

# TODO: get number of audiences
# TODO: list title into csv


class GetRooms:
    def __init__(self, file):
        self.workbook = AdminWorkbook(file)

    def get_base_url(self):
        base_url = self.workbook.read_cell('设置','B2')
        return base_url

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
                return self.workbook.read_cell('主题列表', 'B%d' % row)
            else:
                continue

    def get_room_list(self, no):
        home = self.get_topic_url(no)
        page_soup = self.get_page_soup(home)
        live_rooms = page_soup.find("ul", attrs={"class": "live-list clearfix"})
        total_rooms = len(live_rooms.find_all('a', class_='title new-clickstat', href=True))

        print(total_rooms)
        hrefs = []

        for a in live_rooms.find_all('a', class_='title new-clickstat', href=True):
            print(a['href'], a['title'])
            hrefs.append(a['href'])

        df = pd.DataFrame(np.array(hrefs))
        df.to_csv('../room_list.csv')


if __name__ == '__main__':
    t = GetRooms()
    t.get_room_list(2)

import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re
import os


# TODO: get number of audiences
# TODO: list title into csv



def get_game_url(num):
    base_url = "http://www.huya.com/g/"
    url = base_url + str(num)
    print(url)
    return url


def get_room_list():
    for i in range(1,2): # TODO:
        # home = "http://www.huya.com/g/4"
        home = get_game_url(4)
        # 模拟请求头
        headers = {
            "Host": "www.huya.com",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"
        }
        # 构造好请求对象 将请求提交到服务器 获取的响应就是到首页的html代码
        request = urllib.request.Request(url=home, headers=headers)
        response = urllib.request.urlopen(request)
        page_soup = BeautifulSoup(response.read(), "lxml")
        live_rooms = page_soup.find("ul", attrs={"class": "live-list clearfix"})
        total_rooms = len(live_rooms.find_all('a', class_='title new-clickstat', href=True))
        # total_rooms = len(live_rooms.find_all('li', class_='game-live-item'))

        print(total_rooms)
        hrefs = []

        for a in live_rooms.find_all('a', class_='title new-clickstat', href=True):
            print(a['href'], a['title'])
            hrefs.append(a['href'])

        df = pd.DataFrame(np.array(hrefs))
        df.to_csv('../room_list.csv')


if __name__ == '__main__':
    # test()
    get_room_list()






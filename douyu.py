import re
import urllib.request as ur
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup

TOTAL_PAGES = 1

class DySpyder():

    def __init__(self):
        self.url = self.get_url()

    def get_url(self):
        for page in [j + 1 for j in range(TOTAL_PAGES)]:
            return "https://www.douyu.com/directory/all?page="+ str(page) +"&isAjax=1"

    def open_url(self):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
        req = ur.Request(url=self.url, headers=headers)
        response = ur.urlopen(req)
        return response.read().decode('utf-8')

    def from_url_get_all_lis(self):
        data = self.open_url()
        soup = BeautifulSoup(data, 'html.parser').findAll("li")
        return soup

    def tv_spyder(self, x):
        rid = re.findall(""".*?data-rid="(.*?)".*""", str(x))[0]
        title = re.findall(""".*?title=(.*?)>.*""", str(x))[0]
        href = re.findall(""".*?href="(.*?)".*""", str(x))[0]
        # pic = re.findall('''.*?<img data-original="(.*?)".*''', str(x))[0]
        tag = re.findall('''.*<span class="tag ellipsis">(.*?)</span>.*''', str(x))[0]
        name = re.findall('''.*<span class="dy-name ellipsis fl">(.*?)</span>.*''', str(x))[0]
        see_num = re.findall(""".*<span class="dy-num fr".*?>(.*?)</span>.*""", str(x))[0]
        t = rid,  title, tag, name, see_num, href
        return t




if __name__ == '__main__':
    res1 = []
    douyu = DySpyder()
    print(douyu.from_url_get_all_lis())
    for x in douyu.from_url_get_all_lis():
        try:
            res1.append(list(douyu.tv_spyder(x)))
        except:
            print("Fail...")

    df = pd.DataFrame(np.array(res1))
    df.to_csv("demo.csv")
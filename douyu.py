import re
import urllib.request as ur
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup

class DySpyder():

    def __init__(self, url):
        self.url = url
        self.soup =""

    def open_url(self, url):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
        req = ur.Request(url=url, headers=headers)  # python2，urllib.request()
        response = ur.urlopen(req)  # python2，urllib2.urlopen()
        return response.read().decode('utf-8')

    def from_url_get_all_lis(self):
        data = self.open_url(self.url)
        self.soup = BeautifulSoup(data, 'html.parser')
        soup = self.soup.findAll("li")
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

def get_url(page):
    return "https://www.douyu.com/directory/all?page="+ str(page) +"&isAjax=1"


if __name__ == '__main__':
    res1 = []
    for i in [j + 1 for j in range(1)]:
        douyu = DySpyder(get_url(i))

        print(douyu.from_url_get_all_lis())
        for x in douyu.from_url_get_all_lis():
            try:
                res1.append(list(douyu.tv_spyder(x)))
            except:
                print("Fail...")

    df = pd.DataFrame(np.array(res1))
    df.to_csv("demo.csv")
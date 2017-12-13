import re
import urllib.request as ur
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup

TOTAL_PAGES = 2


class DySpyder:

    def get_url(self,page):
        print("https://www.douyu.com/directory/all?page=" + str(page) + "&isAjax=1")
        return "https://www.douyu.com/directory/all?page=" + str(page) + "&isAjax=1"

    def open_url(self,page):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
        req = ur.Request(url=self.get_url(page), headers=headers)
        response = ur.urlopen(req)
        return response.read().decode('utf-8')

    def from_url_get_all_lis(self,page):
        data = self.open_url(page)
        soup = BeautifulSoup(data, 'html.parser').findAll("li")
        return soup

    def tv_spyder(self, soup):
        rid = re.findall(""".*?data-rid="(.*?)".*""", str(soup))[0]
        title = re.findall(""".*?title=(.*?)>.*""", str(soup))[0]
        href = re.findall(""".*?href="(.*?)".*""", str(soup))[0]
        # pic = re.findall('''.*?<img data-original="(.*?)".*''', str(x))[0]
        tag = re.findall('''.*<span class="tag ellipsis">(.*?)</span>.*''', str(soup))[0]
        name = re.findall('''.*<span class="dy-name ellipsis fl">(.*?)</span>.*''', str(soup))[0]
        see_num = re.findall(""".*<span class="dy-num fr".*?>(.*?)</span>.*""", str(soup))[0]
        info = rid,  title, tag, name, see_num, href
        return info

    def export(self):
        list_anchor = []
        for page in range(1, TOTAL_PAGES + 1):
            for soup in self.from_url_get_all_lis(page):
                try:
                    list_anchor.append(list(self.tv_spyder(soup)))
                except:
                    print("Fail...")

        df = pd.DataFrame(np.array(list_anchor))
        df.to_csv('demo.csv')


if __name__ == '__main__':
    douyu = DySpyder()
    douyu.export()


    # def save(self):
    #     for soup in self.soups:
    #         try:
    #             self.list_anchor.append(list(douyu.tv_spyder(soup)))
    #         except:
    #             print("Fail...")
    #
    # def export(self):
    #     self.save()
    #     return self.list_anchor
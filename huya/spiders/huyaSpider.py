# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from huya.items import HuyaItem
import urllib.request
import openpyxl
from bs4 import BeautifulSoup
from scrapy.http import Request
from huya.spiders.admin_excel import AdminWorkbook
from huya.spiders.get_rooms import GetRooms


class HuyaSpider(CrawlSpider):
    name = 'huya'
    allowed_domains = ["huya.com"]
    start_urls = ['https://www.huya.com/g/xingxiu']
    file_path = 'G:\Program\Projects\Live_Sipder\huya.xlsx'
    workbook = AdminWorkbook(file_path)
    get_room = GetRooms(file_path)
    total_rooms = 0

    def start_requests(self):
        url = self.get_room.get_topic_url(1+1)
        print('url: '+url)
        yield Request('https://www.huya.com/g/xingxiu', callback=self.parse)


    def parse(self, response):
        self.workbook.load_workbook()
        live_rooms = response.xpath('//ul[@class="live-list clearfix"]/li//a[@class="title new-clickstat"]/@herf')
        # live_rooms = page_soup.find("ul", attrs={"class": "live-list clearfix"})
        # total_rooms_in_page = len(live_rooms.find_all('a', class_='title new-clickstat', href=True))
        #
        # current_total_rooms_in_topic = self.total_rooms + total_rooms_in_page
        print(live_rooms)
        for room in live_rooms:
            item = HuyaItem()
            item['room'] = room # .xpath('.//a[@class="title new-clickstat"]/@herf')
            print(item['room'])
        # r = 1
        # for a in live_rooms.find_all('a', class_='title new-clickstat', href=True):
        #     print(a['href'], a['title'])
        #     if self.total_rooms + r <= current_total_rooms_in_topic:
        #         print(self.total_rooms + r)
        #         self.workbook.write_cell(self.topic, 'A%d' % (self.total_rooms + r), a['title'])
        #         self.workbook.write_cell(self.topic, 'B%d' % (self.total_rooms + r), a['href'])
        #         r += 1


        # movies = response.xpath('//ul[@class="game-list clearfix"]/li')
        # i = 1
        # for each_movie in movies:
        #     item = HuyaItem()
        #     item['topic'] = each_movie.xpath('./a/img/@title').extract()[0]
        #     item['href'] = each_movie.xpath('./a/@href').extract()[0]
        #     print(item['topic'])
        #     self.workbook.write_cell('主题列表', 'A%d' % i, item['topic'])
        #     self.workbook.write_cell('主题列表', 'B%d' % i, item['href'])
        #     i = i + 1
        #     yield item
        #     self.workbook.save_workbook()

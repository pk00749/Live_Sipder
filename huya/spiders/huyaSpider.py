# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from huya.items import HuyaItem
import urllib.request as ur
import requests
import json
from bs4 import BeautifulSoup as bs
import itertools
from scrapy.http import Request, HtmlResponse
from huya.spiders.admin_excel import AdminWorkbook
from huya.spiders.get_rooms import GetRooms


class HuyaSpider(CrawlSpider):
    name = 'huya'
    total_rooms = 0
    no = 2
    file_path = 'G:\Program\Projects\Live_Sipder\huya.xlsx'
    get_room = GetRooms(file_path)
    workbook = AdminWorkbook(file_path)
    allowed_domains = ["huya.com"]
    base_url = 'https://www.huya.com/g/'
    start_urls = ['https://www.huya.com/g/']
    room_base_url = 'https://www.huya.com/'


    def start_requests(self):
        # url = self.get_room.get_topic_url(1+1)
        for url in self.start_urls:
            print('url: '+url)
            yield Request(url, callback=self.parse)


    def parse(self, response):
        self.logger.info("parse, Visited %s", response.url)
        movies = response.xpath('//ul[@class="game-list clearfix"]/li')
        topic = self.workbook.read_cell('登录', 'C%d' % self.no)
        print('topic: ' + topic)
        self.workbook.create_sheet(topic)
        for each_movie in movies:
            if topic == each_movie.xpath('./a/img/@title').extract()[0]:
                gid = each_movie.xpath('./@gid').extract()[0]
                print(each_movie.xpath('./@gid').extract()[0])
                href = each_movie.xpath('./a/@href').extract()[0]
                print('href: ' + href)
                yield Request(href, callback=self.page, meta={'gid': gid})


    def page(self, response):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
        total_pages = response.xpath('//div[@class="list-page"]/@data-pages').extract()[0]
        print(total_pages)
        for p in range(1, int(total_pages) + 1):
            url = self.topic_url_by_page(response.meta['gid'], p)
            print('parse, url: ' + url)
            # req = ur.Request(url, headers=headers)
            # resp = ur.urlopen(req)
            # print(resp.read().decode('utf-8'))
            # re = Request(url, callback=self.get_topic_url)
            yield Request(url, callback=self.get_room_url)


    def topic_url_by_page(self, gid, page):
        return 'https://www.huya.com/cache.php?m=LiveList&do=getLiveListByPage&gameId={gid}&tagAll=0&page={page}'.format(
            gid=gid, page=page)


    def get_room_url(self, response):
        self.logger.info("get_topic_url Visited %s", response.url)
        body = response.body
        body_str = body.decode()
        body_json = json.loads(body_str)
        total_rooms_by_page = len(body_json['data']['datas'])
        self.total_rooms += total_rooms_by_page
        for room in range(0, total_rooms_by_page):
            room_id = body_json['data']['datas'][room]['profileRoom']
            room_url = self.room_base_url+ room_id
            print(room_url)
            yield Request(room_url, callback=self.send_msgs)

        print('---------total rooms: '+ str(self.total_rooms))


    def send_msgs(self, response):
        self.logger.info("send msgs, Visited %s", response.url)












    # live_rooms = response.xpath(
    #     '//ul[@class="live-list clearfix"]/li/a[@class="title new-clickstat"]/@href').extract()
    # total_rooms_in_page = len(live_rooms.find_all('a', class_='title new-clickstat', href=True))
    #
    # current_total_rooms_in_topic = self.total_rooms + total_rooms_in_page
    # print(live_rooms)
    # for room in live_rooms:
    #     item = HuyaItem()
    #     item['room'] = room  # .xpath('.//a[@class="title new-clickstat"]/@herf')
    #     print(item['room'])


        # self.workbook.load_workbook()
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

# -*- coding: utf-8 -*-
import scrapy
import sys
sys.path.append('../')
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from huya.items import HuyaItem
import json, os, pymongo
from scrapy.http import Request
from selenium import webdriver
from huya.spiders.config import USER_PROFILE
from scrapy.conf import settings


class HuyaSpiderSpider(CrawlSpider):
    name = 'huya'
    allowed_domains = ['huya.com']
    start_urls = ['https://www.huya.com/g/']
    total_rooms = 0
    no = 2
    base_url = 'https://www.huya.com/g/'
    room_base_url = 'https://www.huya.com/'

    def __init__(self, *args, **kwargs):  # user_name
        self.logger.info(__name__)
        print(__name__)
        super(HuyaSpiderSpider, self).__init__(*args, **kwargs)
        self.user_info = kwargs.get('user')
        self.user_name = self.user_info.get('user_name')
        # self.user_name = '13250219510'#TODO:Testing
        print('Spider initialing, user name: {user_name}'.format(user_name=self.user_name))  # % str(self.user_name))
        user_profile = USER_PROFILE(self.user_name)
        self.user_info = user_profile.get_user_profile()
        self.topic = self.user_info['topic']
        print(str(self.topic))

        self.conn = pymongo.MongoClient(settings['MONGODB_HOST'], settings['MONGODB_PORT'])
        self.db = self.conn[str(settings['MONGODB_DB_NAME'])]
        self.db['rooms'].remove({})
        print(self.db['rooms'].count())
        # ----------------------------
        # chromedriver = "C:\Program Files\Google\Chrome\Application\chromedriver.exe"
        # os.environ["webdriver.chrome.driver"] = chromedriver
        # option = webdriver.ChromeOptions()
        # self.driver = webdriver.Chrome(chromedriver, chrome_options=option)
        service_args = []
        # service_args.append('--load-image=no') # useless
        service_args.append('--disk-cache=yes')
        service_args.append('--ignore-ssl-errors=true')
        self.driver = webdriver.PhantomJS(service_args=service_args)
        self.driver.maximize_window()

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, callback=self.parse)

    def parse(self, response):
        self.logger.info("METHOD - parse, visited by %s", response.url)
        # print(response.body.decode())
        # print(response)
        all_topics = response.xpath('//li[@class="game-list-item"]')
        print('Number of togics:' + str(len(all_topics)))
        topic = '绝地求生'  # json.get('topic')

        for each_topic in all_topics:
            if topic == each_topic.xpath('./a/img/@title').extract()[0]:
                self.logger.info('Topic: ' + topic)
                gid = each_topic.xpath('./@gid').extract()[0]
                self.logger.info('ID: ' + gid)
                topic_href = each_topic.xpath('./a/@href').extract()[0]
                self.logger.info("URL of the topic: " + topic_href)
                yield Request(topic_href, callback=self.page, meta={'gid': gid})

    @staticmethod
    def topic_url_by_page(gid, page):
        return 'https://www.huya.com/cache.php?m=LiveList&do=getLiveListByPage&gameId={gid}&tagAll=0&page={page}'.format(
            gid=gid, page=page)

    def page(self, response):
        self.logger.info("METHOD - page, visited by %s", response.url)
        total_pages = response.xpath('//div[@class="list-page"]/@data-pages').extract()[0]
        self.logger.info("Total pages of the topic: " + total_pages)

        for p in range(1, int(total_pages) + 1):
            url = self.topic_url_by_page(response.meta['gid'], p)
            yield Request(url, callback=self.get_room_url)

    def get_room_url(self, response):
        self.logger.info("METHOD - get_topic_url, visited by %s", response.url)
        items = HuyaItem()
        body_json = json.loads(response.body)
        total_rooms_by_page = len(body_json['data']['datas'])
        print('now: ' + str(self.total_rooms))
        for room in range(0, total_rooms_by_page):
            room_id = body_json['data']['datas'][room]['profileRoom']
            audiences = body_json['data']['datas'][room]['totalCount']
            items['_id'] = room_id
            items['room'] = room_id
            items['audiences'] = int(audiences)
            items['status'] = 'p'
            yield items
        self.total_rooms = self.total_rooms + total_rooms_by_page
        self.logger.info('Total rooms: ' + str(self.total_rooms))
        print('Total rooms: ' + str(self.total_rooms))

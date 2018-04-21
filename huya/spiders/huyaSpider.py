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
from scrapy.http import Request, HtmlResponse
from huya.spiders.admin_excel import AdminWorkbook
from huya.spiders.get_rooms import GetRooms
import websocket, _thread, time
import socket
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


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
    driver = webdriver.PhantomJS()
    driver.maximize_window()
    driver.implicitly_wait(30)  # 隐式等待


    def start_requests(self):
        # url = self.get_room.get_topic_url(1+1)
        for url in self.start_urls:
            # print('url: '+url)
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
                # print(each_movie.xpath('./@gid').extract()[0])
                href = each_movie.xpath('./a/@href').extract()[0]
                # print('href: ' + href)
                yield Request(href, callback=self.page, meta={'gid': gid})

    def page(self, response):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
        total_pages = response.xpath('//div[@class="list-page"]/@data-pages').extract()[0]
        # print(total_pages)
        for p in range(1, int(total_pages) + 1):
            url = self.topic_url_by_page(response.meta['gid'], p)
            # print('parse, url: ' + url)
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
            room_url = self.room_base_url + room_id
            # print(room_url)
            yield Request(room_url, callback=self.is_login, meta={'url': room_url})

        print('---------total rooms: ' + str(self.total_rooms))


    def is_login(self, response):
        login_name = response.xpath('//span[@id="login-username"]/@title').extract()
        # print(response.xpath('//span[@id="login-username"]/@title').extract()[0])
        if login_name:
            print('NO need to login')
            print(login_name)
            # self.send_advertisement()
        else:
            print("Need to login")
            print(login_name)
            self.login(response.meta['url'])
            # self.send_advertisement()

    def login(self, url):
        driver = self.driver
        driver.get(url)
        print('url: '+url)
        __username = '13250219510'
        __password = '81302137hy'
        title = driver.title
        print(title)

        # driver.find_element_by_link_text("登录").click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'nav-login'))).click()
        # self.driver.find_element_by_id('nav-login').click()
        WebDriverWait(driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//*[@id='udbsdk_frm_normal']")))
        # frame = driver.find_element_by_xpath("//*[@id='udbsdk_frm_normal']")
        # driver.switch_to.frame(frame)
        time.sleep(1)

        ele = driver.find_element_by_xpath("//*[@id='m_commonLogin']/div[1]/span/input")
        ele.send_keys(__username)

        ele = driver.find_element_by_xpath("//*[@id='m_commonLogin']/div[2]/span/input")
        ele.send_keys(__password)

        time.sleep(1)
        driver.find_element_by_xpath("//*[@id='m_commonLogin']/div[5]/a[1]").click()

        # Cookie1 = response.headers.getlist('Set-Cookie')  # 查看一下响应Cookie，也就是第一次访问注册页面时后台写入浏览器的Cookie
        # print(Cookie1)

        print("Login success")
        time.sleep(2)
        driver.switch_to.default_content()  # switch to main page










    # def send_msgs(self, response):
    #     self.logger.info("send msgs, Visited %s", response.url)

    # def on_message(ws, message):
    #     print(message)

    # def on_error(ws, error):
    #     print(error)

    # def on_close(ws):
    #     print('### closed ###')

    # def on_open(ws):
    #     def run(*args):
    #         for i in range(3):
    #             time.sleep(1)
    #             ws.send("hello %d" % i)
    #         time.sleep(1)
    #         ws.close()
    #         print("thread terminating...")
    #     _thread.start_new_thread(run, ())

# <span class="btn-sendMsg hiido_stat" id="msg_send_bt" hiido_code="10004279">发送</span>








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

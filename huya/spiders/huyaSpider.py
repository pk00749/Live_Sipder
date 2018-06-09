import sys
sys.path.append('..')
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from huya.items import HuyaItem
import json, pickle, os
from scrapy.http import Request, HtmlResponse
from selenium import webdriver


class HuyaSpider(CrawlSpider):

    name = 'huya'
    total_rooms = 0
    no = 2
    allowed_domains = ["huya.com"]
    base_url = 'https://www.huya.com/g/'
    start_urls = ['https://www.huya.com/g/']
    room_base_url = 'https://www.huya.com/'

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.a = a
        # chromedriver = "C:\Program Files\Google\Chrome\Application\chromedriver.exe"
        # os.environ["webdriver.chrome.driver"] = chromedriver
        # option = webdriver.ChromeOptions()
        # self.driver = webdriver.Chrome(chromedriver, chrome_options=option)
        service_args = []
        # service_args.append('--load-image=no')
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
        all_topics = response.xpath('//li[@class="game-list-item"]')
        print('Number of togics:' + str(len(all_topics)))
        # json = self.load_json()
        topic = '绝地求生' #json.get('topic')

        for each_topic in all_topics:
            if topic == each_topic.xpath('./a/img/@title').extract()[0]:
                self.logger.info('Topic: ' + topic)
                gid = each_topic.xpath('./@gid').extract()[0]
                self.logger.info('ID: ' + gid)
                topic_href = each_topic.xpath('./a/@href').extract()[0]
                self.logger.info("URL of the topic: " + topic_href)
                yield Request(topic_href, callback=self.page, meta={'gid': gid, "cookiejar": 123})

    def page(self, response):
        self.logger.info("METHOD - page, visited by %s", response.url)
        total_pages = response.xpath('//div[@class="list-page"]/@data-pages').extract()[0]
        self.logger.info("Total pages of the topic: " + total_pages)

        for p in range(1, int(total_pages) + 1):
            url = self.topic_url_by_page(response.meta['gid'], p)
            yield Request(url, callback=self.get_room_url, meta={"cookiejar": 123})

    def topic_url_by_page(self, gid, page):
        return 'https://www.huya.com/cache.php?m=LiveList&do=getLiveListByPage&gameId={gid}&tagAll=0&page={page}'.format(
            gid=gid, page=page)

    def get_room_url(self, response):
        self.logger.info("METHOD - get_topic_url, visited by %s", response.url)
        items = HuyaItem()
        body = response.xpath('//body/text()').extract()[0]
        body_json = json.loads(body)
        total_rooms_by_page = len(body_json['data']['datas'])
        self.total_rooms += int(total_rooms_by_page)
        for room in range(0, total_rooms_by_page):
            room_id = body_json['data']['datas'][room]['profileRoom']
            items['_id'] = room
            items['room'] = room_id
            items['status'] = 'p'
            yield items
        self.logger.info('Total rooms: ' + str(self.total_rooms))

    # def load_json(self):
    #     return pickle.load(open("./json/temp.pkl", "rb"))



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



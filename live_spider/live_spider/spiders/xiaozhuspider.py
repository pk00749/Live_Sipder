import scrapy
import sys
sys.path.append('..')

from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.http import Request
from live_spider.items import LiveSpiderItem


class xiaozhu(CrawlSpider):
    name = 'xiaozhu'
    start_urls = ['http://bj.xiaozhu.com/search-duanzufang-p1-0/']

    def parse(self, response):
        item = LiveSpiderItem()
        selector = Selector(response)
        commoditys = selector.xpath('//ul[@class="pic_list clearfix"]/li')
        for commodity in commoditys:
            address = commodity.xpath('div[2]/div/a/span/text()').extract()[0]

            item['address'] = address

            yield item

        urls = ['http://bj.xiaozhu.com/search-duanzufang-p{}-0/'.format(str(i)) for i in range(1, 14)]
        for url in urls:
            yield Request(url, callback=self.parse)
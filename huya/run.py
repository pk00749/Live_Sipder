from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from spiders.huya_spider import HuyaSpiderSpider
from huya.spiders.in_rooms import conphantomjs
import sys
from scrapy import cmdline

account = int(sys.argv[1])
if account:
    spider = CrawlerProcess(get_project_settings())
    spider.crawl(HuyaSpiderSpider, user={'user_name':account})
    spider.start()
    # cmdline.execute("scrapy crawl huya -a user_name={user}".format(user=user).split())
else:
    print('no user')
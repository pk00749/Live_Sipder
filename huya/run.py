import sys, os
sys.path.append(os.getcwd())
sys.path.append('..')
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from spiders.huya_spider import HuyaSpiderSpider
from huya.spiders.in_rooms import conphantomjs

from scrapy import cmdline
import logging

if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    account = int(sys.argv[1])
    if account:
        # print('user_name: '+ str(account))
        # logging.info('user_name: '+ str(account))
        # spider = CrawlerProcess(get_project_settings())
        # spider.crawl(HuyaSpiderSpider, user={'user_name':account})
        # spider.start()
        # print('The latest list of rooms extracted....')
        # logging.info('The latest list of rooms extracted....')
        # cmdline.execute("scrapy crawl huya -a user_name={user}".format(user=user).split())
        logging.info('Start to send massage to each room')
        con = conphantomjs(int(sys.argv[1]))
        con.main()
    else:
        print('no user')
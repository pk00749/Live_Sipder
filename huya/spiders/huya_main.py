from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from huya.spiders.huya_spider import HuyaSpiderSpider

spider = CrawlerProcess(get_project_settings())
spider.crawl(HuyaSpiderSpider, user={'user_name':13250219510})
spider.start()


# start_huya_spider()

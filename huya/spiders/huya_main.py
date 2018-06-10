from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from huya.spiders.huya_spider import HuyaSpiderSpider

def start_huya_spider():
    # a = HuyaSpiderSpider()
    process = CrawlerProcess(get_project_settings())
    process.crawl(HuyaSpiderSpider)
    process.start()


start_huya_spider()

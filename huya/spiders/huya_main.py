from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from huya.spiders.huyaSpider import HuyaSpider


def start_huya_spider():
    process = CrawlerProcess(get_project_settings())
    process.crawl(HuyaSpider)
    process.start()

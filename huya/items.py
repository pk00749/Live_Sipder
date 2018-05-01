# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HuyaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    topic = scrapy.Field()
    topic_url = scrapy.Field()
    room = scrapy.Field()
    room_url = scrapy.Field()
    pass

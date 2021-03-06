# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sys
from logging import getLogger
import pymongo
from scrapy import Item
from scrapy.conf import settings


class HuyaPipeline(object):

    def __init__(self):
        print('pipeline init...')
        self.logger = getLogger(__name__)
        try:
            self.conn = pymongo.MongoClient(settings['MONGODB_HOST'], settings['MONGODB_PORT'])
            self.db = self.conn[settings['MONGODB_DB_NAME']]
            # TODO: regular remove

        except ConnectionError:
            print('Connect Database Fail...')
            sys.exit(1)

    def close_spider(self, spider):
        print(self.db['rooms'].count())
        self.conn.close()

    def insert_db(self, item):

        if isinstance(item, Item):
            item = dict(item)
        try:
            self.db['rooms'].insert_one(item)
            print('inserted')
        except Exception:
            print('Duplicated key')

    def process_item(self, item, spider):
        self.insert_db(item)


if __name__ == "__main__":
    my_conn = HuyaPipeline()
    # my_conn.db['rooms'].remove({})
    # print(my_conn.db['rooms'].count())
    # result = my_conn.db['rooms'].find({}).limit(15).sort('audiences', pymongo.DESCENDING)
    # print(result)
    # for i in result:
    #     print(i)
    all = my_conn.db['rooms'].find({}).sort('audiences', pymongo.DESCENDING)
    print(all)
    for i in all:
        print(i)
    # one = my_conn.db['rooms'].find_one({'room':'752288'})
    # print(one)

    # all = my_conn.db['rooms'].find({})
    # i = 0
    # for a in all:
    #     print(a['room'])
    #     i += 1
    #     if i == 10:
    #         print('----')
    #         i = 0
        # else:continue

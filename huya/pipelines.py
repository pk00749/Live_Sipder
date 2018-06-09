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
    phantomjs_max = 1  # 同时开启phantomjs个数
    jiange = 0.00001  # 开启phantomjs间隔
    timeout = 20  # 设置phantomjs超时时间

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
        self.conn.close()

    def insert_db(self, item):

        if isinstance(item, Item):
            item = dict(item)
        self.db['rooms'].insert_one(item)

    def process_item(self, item, spider):
        self.insert_db(item)


if __name__ == "__main__":
    my_conn = HuyaPipeline()
    count = my_conn.db['rooms'].count()
    print(count)
    res = my_conn.db['rooms'].find({})
    for k in res:
        print(k)
    # for e in range(0, count//10+1):
    #     print('---------------%d' % e)
    #     res = my_conn.db['rooms'].find({'_id': {'$gte': 10*e, '$lt': 10*(e+1)}})
    #     for k in res:
    #         print(k)
    #         urls.append(k['room'])
    #     print(urls)
    #     print('---------------')

    # datas = [
    #     {'_id':1, 'data':12},
    #     {'_id':2, 'data':22},
    #     {'_id':3, 'data':'cc'}
    # ]
    # 插入数据，'mytest'是上文中创建的表名
    # my_conn.db['rooms'].insert(datas)
    # 查询数据，'mytest'是上文中创建的表名

# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class HuyaPipeline(object):
    # def process_item(self, item, spider):
    #     return item
    def process_item(self, item, spider):
        # with open("huya.txt",'a') as fp:
        #     fp.write(item['topic'] + '\n')
        return item
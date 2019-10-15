# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json

class SpiderDynamicPipeline(object):
    def __init__(self, fpath):
        self.fpath = fpath
        print(self.fpath)

    def open_spider(self, spider):  # spider开始前调用
        print("call open_spider")
        self.save = open(self.fpath, "w", encoding='utf-8')

    def close_spider(self, spider):  # spider结束后调用
        print("close spider")
        self.save.close()

    def process_item(self, item, spider):
        info = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.save.write(info)
        return item

    @classmethod
    def from_crawler(cls, crawler):
        # FirstprojectJsonPipeline(fpath)
        return cls(fpath=crawler.settings.get("JSON_PATH"))

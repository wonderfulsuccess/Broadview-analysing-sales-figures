# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs
import json
import os
from bookinfo.spiders.amazonbook import AmazonBookSpider
from bookinfo.spiders.dangdangbook import DangdangbookSpider
from scrapy.exceptions import DropItem


class BookinfoPipeline(object):

    def __init__(self):
        if os.path.exists('./bookdata/data.txt'):
            with open('./bookdata/data.txt', 'r', encoding='utf-8') as old:
                if old.read() != '[0]':
                    os.rename('./bookdata/data.txt', './bookdata/data_old.txt')

        self.file = codecs.open('./bookdata/data.txt', 'w', encoding='utf-8')

        # 创建一个json list
        self.file.writelines("[")
        # 统计爬去图书总数 最后写入文档尾部
        self.book_counter = 0

    def process_item(self, item, spider):
        if isinstance(spider, DangdangbookSpider) and item:
            print('is instance haha')
            json.dump({
                'coverImage':item['coverImage'],
                'classify':item['classify'],
                'index':item['index'],
                'pageNo':item['pageNo'],
                'content':item['content'],
                }, self.file, indent=4)
            self.file.writelines(",\n")
            self.book_counter += 1
            raise DropItem('amazon data has deal: %s' % item)
        else:
            return item

    def close_spider(self, spider):
        self.file.writelines(str(self.book_counter)+"]")
        self.file.close()


class AmazonBookInfoPipeline(object):

    def __init__(self):
        if os.path.exists('./bookdata/amazon_data.jl'):
            with open('./bookdata/amazon_data.jl', 'r', encoding='utf-8') as old:
                if old.read() != '[0]':
                    os.rename('./bookdata/amazon_data.jl', './bookdata/amazon_data_old.jl')
        self.file = codecs.open('./bookdata/amazon_data.jl', 'w', encoding='utf-8')
        self.file.writelines("[")
        self.book_counter = 0

    def close_spider(self, spider):
        self.file.writelines(str(self.book_counter) + ']')
        self.file.close()

    def process_item(self, item, spider):
        if isinstance(spider, AmazonBookSpider) and item:
            jsons = json.dumps({
                'coverImage': item['coverImage'],
                'classify': item['classify'],
                'index': item['index'],
                'pageNo': item['pageNo'],
                'content': item['content'],
            }) + ',\n'
            self.file.write(jsons.encode('utf-8').decode('unicode_escape'))
            self.book_counter += 1
            raise DropItem('amazon data has deal: %s' % item)
        else:
            return item

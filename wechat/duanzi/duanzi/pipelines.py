# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from .MysqlConnect import MysqlHelper


class DuanziPipeline(object):
    def process_item(self, item, spider):
        article = item['article']
        if len(article) < 255:
            db = MysqlHelper(mysqldb='duanzi')
            sql = "insert into articles(article) values (%s)"
            params = (item['article'],)
            db.insert(sql, params=params)
            db.close()
        return item

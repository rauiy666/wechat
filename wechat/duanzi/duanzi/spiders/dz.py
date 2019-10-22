# -*- coding: utf-8 -*-
import scrapy

from ..items import DuanziItem


class DzSpider(scrapy.Spider):
    name = 'dz'
    allowed_domains = ['duanziwang.com']
    base_url = "http://duanziwang.com/page/{}/"
    page = 1
    start_urls = [base_url.format(str(page))]

    def parse(self, response):
        articles = response.xpath("//article[@class='post']")
        if articles:
            for a in articles:
                head = a.xpath("./div[@class='post-head']/h1/a/text()").get()
                content = a.xpath("./div[@class='post-content']/p/text()").get()
                a_id = a.xpath("./@id").get()
                if a_id == "1":
                    continue
                if content:
                    article = content
                else:
                    article = head
                item = DuanziItem()
                item['article'] = article

                yield item
            self.page += 1
            url = self.base_url.format(str(self.page))
            yield scrapy.Request(url, callback=self.parse)

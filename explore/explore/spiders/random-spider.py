# -*- coding: utf-8 -*-
import scrapy


class RandomdSpider(scrapy.Spider):
    name = "randomd"
    allowed_domains = ["baidu.com"]
    start_urls = ['http://baidu.com/']

    def parse(self, response):
        print(response.xpath('//title'))
        pass

# -*- coding: utf-8 -*-
import scrapy


class ZycgSpider(scrapy.Spider):
    name = "zycg"
    allowed_domains = ["ccgp.gov.cn/zycg"]
    start_urls = ['http://www.ccgp.gov.cn/zycg/']


    def parse(self, response):
        with open("zycg1.html","a+") as f:
            f.write(response.body)
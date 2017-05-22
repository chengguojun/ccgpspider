# -*- coding: utf-8 -*-
import datetime
import os
import random
import re
from time import sleep, time

import requests
import scrapy
from bs4 import BeautifulSoup
from scrapy import Request
from ccgp import settings

import sys

from ccgp.items import CcgpItem

reload(sys)
sys.setdefaultencoding('utf-8')


class ZycgSpider(scrapy.Spider):
    name = "zycg"
    allowed_domains = ["ccgp.gov.cn"]
    start_urls = []

    # 添加cookies，headers

    cookie = {
        "JSESSIONID": "SToqROwgKXg7MMs9_geqsaAwJBelMh6VeZxxysJ4OztIX6RRhGSe!107352958",
        "_gscu_273633028": "951027415ixbz628",
        "Hm_lvt_9f8bda7a6bb3d1d7a9c7196bfed609b5": "1495246733,1495248328,1495290061,1495357781",
        "Hm_lpvt_9f8bda7a6bb3d1d7a9c7196bfed609b5": "1495360190"
    }

    headers = settings.HEADERS
    # meta = settings.META
    meta = {'dont_redirect': True, 'handle_httpstatus_list': [302]}

    def start_requests(self):
        url = 'http://search.ccgp.gov.cn/bxsearch?' \
              'searchtype=1' \
              '&page_index=1' \
              '&bidSort=0' \
              '&buyerName=' \
              '&projectId=' \
              '&pinMu=0' \
              '&bidType=0' \
              '&dbselect=bidx' \
              '&kw=' \
              '&start_time=%s' \
              '&end_time=%s' \
              '&timeType=6' \
              '&displayZone=' \
              '&zoneId=' \
              '&pppStatus=0' \
              '&agentName='

        yield Request(url % ("2017:05:19", "2017:05:22"),
                      callback=self.parse,
                      cookies=self.cookie,
                      meta=self.meta,
                      encoding='utf-8',
                      dont_filter=True
                      )

    def parse(self, response):
        soup = BeautifulSoup(response.body, "lxml", from_encoding="utf-8")
        pages = soup.find_all("p", class_="pager")
        title = soup.select_one("title")
        col_url = response.url
        index = re.findall("page_index=(\d+)", col_url)[0]

        if title.getText() == "302 Found":
            print '>' * 20, title.getText(), '<' * 20
        elif title.getText() == u"标讯库搜索_中国政府采购网":
            print '>' * 20, title.getText(), '<' * 20
            request = Request(url=response.url, cookies=self.cookie, meta=self.meta, callback=self.parse2,
                              dont_filter=True)
            request.meta['PhantomJS'] = True
            yield request

        else:

            # 解析
            ul = soup.find("ul", class_="vT-srch-result-list-bid")
            if ul:
                for li in ul:
                    item = CcgpItem()
                    item['index'] = index
                    hf = li.find('a')
                    if hf != -1:
                        col_title = hf.get_text()
                        print col_title, '*' * 19
                        col_id = hf['href']
                        print col_id, '*' * 20
                        item['col_title'] = col_title
                        item['col_id'] = col_id
                    span = li.find('span')
                    if span != -1:
                        sp_str = span.get_text()
                        cons = sp_str.replace(" ", "").replace("\n", "|").replace("||", "|").split("|")
                        if cons:
                            item['col_publish_time'] = cons[0]
                            item['col_buyer_name'] = cons[1]
                            item['col_agent'] = cons[2]
                            item['col_type'] = cons[3]
                            item['col_zone'] = cons[4]
                            item['col_category'] = cons[5]

                            print 'col_publish_time.....', item['col_publish_time']
                    yield item


        if pages:
            sizes = pages[0].script.getText()
            if sizes:
                size = re.findall(ur"size:(.+?),", sizes)
                if size:
                    pager = int(size[0])  # 总页数
                    print "totalsize......",pager
                    print "index....", index
                    cur_page = int(index)
                    print cur_page, '..........................................'
                    if cur_page < pager:
                        ur = response.url
                        uri = ur.replace("page_index=%s" % re.findall("page_index=(\d+)", ur)[0],
                                         "page_index=%s" % str(cur_page + 1))
                        yield Request(uri, callback=self.parse,
                                      cookies=self.cookie,
                                      # headers=self.headers,
                                      meta=self.meta,
                                      dont_filter=True,
                                      encoding='utf-8')

    def parse2(self, response):
        soup = BeautifulSoup(response.body, "lxml", from_encoding="utf-8")
        pages = soup.find_all("p", class_="pager")
        title = soup.select_one("title")
        col_url = response.url
        index = re.findall("page_index=(\d+)", col_url)[0]
        # 解析
        ul = soup.find("ul", class_="vT-srch-result-list-bid")
        for li in ul:
            item = CcgpItem()
            item['index'] = index
            hf = li.find('a')
            if hf != -1:
                col_title = hf.get_text()
                print col_title, '*' * 19
                col_id = hf['href']
                print col_id, '*' * 20
                item['col_title'] = col_title
                item['col_id'] = col_id
            span = li.find('span')
            if span != -1:
                sp_str = span.get_text()
                cons = sp_str.replace(" ", "").replace("\n", "|").replace("||", "|").split("|")
                if cons:
                    item['col_publish_time'] = cons[0]
                    item['col_buyer_name'] = cons[1]
                    item['col_agent'] = cons[2]
                    item['col_type'] = cons[3]
                    item['col_zone'] = cons[4]
                    item['col_category'] = cons[5]

                    print 'col_publish_time.....', item['col_publish_time']
            yield item



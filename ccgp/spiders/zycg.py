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
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
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
        "__cc_verify__qssec_": "8EpsksRaXkDkgMELzfamfKUXoyDlHAiK",
        "JSESSIONID": "jP4fa_amuhgr_oDuGc8TMyFXVOMka4_2QNDxieTYInDVdWqhNYa2!-509693905",
        "_gscu_273633028": "951027415ixbz628",
        "_gscs_273633028": "951136386bjl1m28|pv:1",
        "_gscbrs_273633028": "1",
        "Hm_lvt_9f8bda7a6bb3d1d7a9c7196bfed609b5": "1495113639,1494986467,1494995720,1495072581",
        "Hm_lpvt_9f8bda7a6bb3d1d7a9c7196bfed609b5": "1495175788"
    }

    headers = settings.HEADERS
    # meta = settings.META
    meta = {'dont_redirect': True, 'handle_httpstatus_list': [302]}

    def start_requests(self):
        # 2016.01-01.31
        # 2016.02-03.31
        start_time = "2017" + "%3A" + "03" + "%3A" + "01"
        end_time = "2017" + "%3A" + "03" + "%3A" + "31"
        url = 'http://search.ccgp.gov.cn/dataB.jsp?' \
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
              '&timeType=2' \
              '&displayZone=' \
              '&zoneId=' \
              '&pppStatus=' \
              '&agentName='

        yield Request(url % (start_time, end_time),
                      callback=self.parse,
                      cookies=self.cookie,
                      # headers=self.headers,
                      meta=self.meta,
                      encoding='utf-8',
                      dont_filter=True
                      )

    def parse(self, response):
        soup = BeautifulSoup(response.body, "lxml", from_encoding="utf-8")
        pages = soup.find_all("p", class_="pager")
        title = soup.select_one("title")

        print title.getText(), '---------------------------'

        if title.getText() == "302 Found":
            print '>' * 20, title.getText(), '<' * 20
        elif title.getText() == u"标讯库搜索_中国政府采购网":
            print '>' * 20, title.getText(), '<' * 20
            print '>' * 20, response.url, '<' * 20
            request = Request(url=response.url, callback=self.parse, dont_filter=True)
            request.meta['PhantomJS'] = True
            yield request

        else:
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

        if pages:
            sizes = pages[0].script.getText()
            if sizes:
                size = re.findall(ur"size:(\d+)", sizes)
                if size:
                    pager = int(size[0]) #总页数
                    # print "size......", pager
                    if index <=pager:
                        ur = response.url
                        uri = ur.replace("page_index=%s" % re.findall("page_index=(\d+)", ur)[0],
                                         "page_index=%s" % str(index+1))
                        yield Request(uri, callback=self.parse,
                                      cookies=self.cookie,
                                      # headers=self.headers,
                                      meta=self.meta,
                                      dont_filter=True,
                                      encoding='utf-8')



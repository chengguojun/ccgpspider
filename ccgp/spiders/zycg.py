# -*- coding: utf-8 -*-
import datetime
import os
import random
import re
from time import sleep

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
    allowed_domains = ["ccgp.gov.cn/zycg"]
    start_urls = []

    # 添加cookies，headers

    cookie = {
        "__cc_verify__qssec_": "QMA9DmGysbMTPMc9Lq6cFNSRcaov5jbw",
        "JSESSIONID": "DBQanmsbyMBjAvA5ed4VLgrjuKX6Px7FfopC1nblyODnQtCMvd5m!-611875121",
        "_gscu_273633028": "948196655cr1vr28",
        "_gscs_273633028": "t95094623n1oyud28|pv:5",
        "_gscbrs_273633028": "1",
        "Hm_lvt_9f8bda7a6bb3d1d7a9c7196bfed609b5": "1494977943,1494986467,1494995720,1495072581",
        "Hm_lpvt_9f8bda7a6bb3d1d7a9c7196bfed609b5": "1495095708"
    }

    headers = settings.HEADERS
    # meta = settings.META
    meta = {'dont_redirect': True, 'handle_httpstatus_list': [302]}

    def start_requests(self):

        start_time = "2013"+"%3A"+"01"+"%3A"+"01"
        end_time = "2013"+"%3A"+"01"+"%3A"+"31"
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
                      encoding='utf-8')

    def parse(self, response):
        soup = BeautifulSoup(response.body, "lxml", from_encoding="utf-8")
        pages = soup.find_all("p", class_="pager")
        title = soup.select_one("title")

        print title.getText(), '---------------------------'
        print title.getText(), '---------------------------'

        if title.getText() == "302 Found" or title.getText() == "403 Forbidden":
            print '>' * 20, title.getText(), '<' * 20
            Request(response.url,
                    callback=self.parse,
                    cookies=self.cookie,
                    # headers=self.headers,
                    meta=self.meta,
                    encoding='utf-8')

        else:
            col_url = response.url
            index = re.findall("page_index=(\d+)", col_url)[0]
            col_name = re.findall("start_time=(.+?)&", col_url.replace(r"%3A", ""))[0]

            # 写出html
            # if os.path.exists("data/html%s" % col_name):
            #     pass
            # else:
            #     os.mkdir("data/html%s" % col_name)
            # with open("data/html%s/%s.html" % (col_name, index), 'a+') as f:
            #     f.write(item['content'])
            # 解析
            ul = soup.find("ul", class_="vT-srch-result-list-bid")
            for li in ul:
                print "当前日期>>>>>>>>>>>>>>>>>>>>>>>>  ", col_name
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
                yield item

        if pages:
            sizes = pages[0].script.getText()
            if sizes:
                size = re.findall(ur"size:(\d+)", sizes)
                if size:
                    pager = int(size[0])
                    print "总共是......", pager
                    for page in range(1, pager + 1):
                        ur = response.url
                        uri = ur.replace("page_index=%s" % re.findall("page_index=(\d+)", ur)[0],
                                         "page_index=%s" % page)

                        yield Request(uri, callback=self.parse,
                                      cookies=self.cookie,
                                      # headers=self.headers,
                                      meta=self.meta,
                                      encoding='utf-8')
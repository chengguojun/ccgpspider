# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
import base64
import random

from scrapy import signals
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

from ccgp.settings import PROXIES
import sys

from ccgp.items import CcgpItem
#
# reload(sys)
# sys.setdefaultencoding('utf-8')


class CcgpSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class RandomUserAgent(object):
    """Randomly rotate user agents based on a list of predefined ones"""

    def __init__(self, agents):
        self.agents = agents

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.getlist('USER_AGENTS'))

    def process_request(self, request, spider):
        # print "**************************" + random.choice(self.agents)
        request.headers.setdefault('User-Agent', random.choice(self.agents))
        request.headers.setdefault('Connection', 'keep - alive')
        request.headers.setdefault('Accept',
                                   'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
        request.headers.setdefault('Accept-Encoding', 'gzip, deflate, sdch')
        # request.headers.setdefault('X-Crawlera-Cookies', 'disable')


class ProxyMiddleware(object):

    @classmethod
    def process_request(self, request, spider):
        proxy = random.choice(PROXIES)
        if proxy.get('level') == u'透明':
            pass
        else:
            print "**************ProxyMiddleware no pass************", proxy.get('address') + ":" + proxy.get('port')
            request.meta['proxy'] = "http://%s:%s" % (proxy.get('address'), proxy.get('port'))


class PhantomJSMiddleware(object):


    @classmethod
    def process_request(cls, request, spider):
        print 'request.....',request
        if request.meta.has_key('PhantomJS'):
            print 'PhantomJS.....'
            desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
            headers = {
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.8',
                'Cache-Control': 'max-age=0',
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
                'Connection': 'keep-alive',
            }
            desired_capabilities["phantomjs.page.settings.loadImages"] = False
            for key, value in headers.iteritems():
                desired_capabilities['phantomjs.page.customHeaders.{}'.format(key)] = value
            driver = webdriver.PhantomJS(executable_path='C:\\developeutils\\developer\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe',
                                         desired_capabilities=desired_capabilities)  # /usr/local/bin/
            try:
                driver.get(request.url)
                content = driver.page_source
            except:
                print "error..."
            finally:
                print 'driver quit...'
                driver.quit()



            return HtmlResponse(request.url, encoding='utf-8', body=content, request=request)

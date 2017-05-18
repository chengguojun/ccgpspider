# -*- coding: utf-8 -*-

# Scrapy settings for ccgp project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'ccgp'

SPIDER_MODULES = ['ccgp.spiders']
NEWSPIDER_MODULE = 'ccgp.spiders'


ROBOTSTXT_OBEY = True
COOKIE={"JSESSIONID":"b64Qa5n3x-vOz5DkjWjvYO-FsA_rjE4qYrnUJCvWNaNM5VCXYO8c!-509693905"," __cc_verify__qssec_":"j12sITOlLX1xjERjVTxXJfx/YCYvgudq"," _gscu_273633028":"948196655cr1vr28","_gscs_273633028":"t94922038e62hmy28|pv:5"," _gscbrs_273633028":"1","Hm_lvt_9f8bda7a6bb3d1d7a9c7196bfed609b5":"1494818756","Hm_lpvt_9f8bda7a6bb3d1d7a9c7196bfed609b5":"1494924114"}
ITEM_PIPELINES = {
    # 'ccgp.pipelines.CcgpPipeline': 100,
    'ccgp.pipelines.MySQLStorePipeline': 800,
}
#start MySql database configure setting
MYSQL_HOST = 'localhost'
MYSQL_DBNAME = 'spider'
MYSQL_USER = 'root'
MYSQL_PASSWD = 'minemine'
#end of MySql database configure setting
HEADERS = {
    'X-Crawlera-Cookies': 'disable',
    'Connection': 'keep - alive',  # 保持链接状态
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'
}
####################################################################

# ########crawlera生效，需要添加你创建的api信息（如果填写了API key的话，pass填空字符串便可）
CRAWLERA_ENABLED = True

CRAWLERA_USER = '<API key>'

CRAWLERA_PASS = 'bc58c892c1e7411c81535cec9a06b1fd'

# ##  为了达到更高的抓取效率，可以禁用Autothrottle扩展和增加并发请求的最大数量，以及设置下载超时
CONCURRENT_REQUESTS = 32

CONCURRENT_REQUESTS_PER_DOMAIN = 32

AUTOTHROTTLE_ENABLED = False

DOWNLOAD_TIMEOUT = 600
#########DOWNLOAD_DELAY的话，需要在setting.py中添加

CRAWLERA_PRESERVE_DELAY = True
##########################################################################

META = {
    'dont_redirect': True,  # 禁止网页重定向
    'handle_httpstatus_list': [301, 302]  # 对哪些异常返回进行处理
}
LOG_ENABLED = True
LOG_ENCODING = 'utf-8'
LOG_FILE = 'ccgp.log'
LOG_LEVEL = 'DEBUG'
LOG_STDOUT = False
#禁用cookies
COOKIES_ENABLED=False

#动态头
USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    # "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    # "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]


#代理ip
PROXIES = [
    {"address": "122.5.129.179", "port": "808", "level": "匿名"},
    {"address": "113.58.234.106", "port": "808", "level": "匿名"},
    {"address": "117.177.241.98","port": "8080", "level": "高匿"},
    {"address": "115.54.247.143","port": "8998", "level": "高匿"},
    {"address": "124.133.230.254","port": "80", "level":"高匿"},
    {"address": "94.23.168.92","port": "24631", "level": "高匿"},
    {"address": "112.17.14.138","port": "8080", "level": "高匿"},
    {"address":"61.147.247.205", "port":"1080","level":"匿名"},
    {"address":"112.84.10.140", "port":"8998","level":"高匿"},
    {"address":"104.131.0.227","port":"3128","level":"透明"},
    {"address":"112.17.14.20","port":"8080","level":"高匿"},
    {"address":"112.17.14.19","port":"8080","level":"高匿"},
    {"address":"112.17.14.44","port":"8080","level":"高匿"},
    {"address":"112.17.14.122","port":"8080","level":"高匿"},
    {"address":"111.23.10.42","port":"8080","level":"高匿"},
    {"address":"111.23.10.11","port":"8080","level":"高匿"},
    {"address":"123.138.43.61","port":"8080","level":"匿名"}
]

DOWNLOAD_DELAY = 1

DOWNLOADER_MIDDLEWARES = {

    'ccgp.middlewares.RandomUserAgent': 1,
    # 'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,
    # 'ccgp.middlewares.ProxyMiddleware': 100,

    # 'scrapy_crawlera.CrawleraMiddleware': 600
}
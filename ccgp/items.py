# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class CcgpItem(Item):
    '''
    采购类
    '''

    col_id = Field()#文章链接地址
    col_title = Field()#采购项目名称
    col_type = Field()#标讯类型
    col_gov_type = Field()#col_gov_type	标讯类别
    col_category = Field()#品目
    col_publish_time = Field()#发布时间
    col_buyer_name = Field()#采购人
    col_projectId = Field()#项目编号
    col_zone = Field()#行政地区
    col_agent = Field()#代理机构
    col_html_content = Field()#网页内容
    # 首页列表
    index = Field()
    url = Field()
    content = Field()







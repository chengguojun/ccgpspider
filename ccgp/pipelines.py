# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re

import MySQLdb.cursors
from twisted.enterprise import adbapi
import os

class CcgpPipeline(object):
    def process_item(self, item, spider):
        # col_time = item.get('url')
        # col_name = re.findall("start_time=(.+?)&", col_time.replace(r"%3A",""))[0]
        # if os.path.exists("data/html%s" % col_name):pass
        # else:os.mkdir("data/html%s" % col_name)
        # with open("data/html%s/%s.html" % (col_name,item['index']), 'a+') as f:
        #     f.write(item['content'])
        return item




class CcgpToMysql(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    # 连接池
    @classmethod
    def from_settings(cls, settings):
        dbargs = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
        return cls(dbpool)

    def process_item(self, item, spider):
        db = self.dbpool.runInteraction(self._do_insert, item, spider)
        db.addErrback(self._handle_error, item, spider)
        db.addBoth(lambda _:item)
        return db

    # 添加入库
    def _do_insert(self, conn, item, spider):

        # index = item.get('index')
        # url = item.get('url')
        # content=item.get('content')
        # conn.ping(True)
        # conn.execute("""
        # insert into ccgp1(indexid,url,content) VALUES (%s,%s,%s)
        # """, (index,url, r"%s" % content.replace("\n","").replace("\r","")))
        if item.get('col_id'):
            conn.execute("""
            INSERT INTO ccgp2
            (col_id,col_title,col_type,col_gov_type,col_category,col_publish_time,col_buyer_name,col_projectId,col_zone,col_agent,col_html_content,col_index)
            VALUES
            (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """,(
            item.get('col_id'),
            item.get('col_title'),
            item.get('col_type'),
            item.get('col_gov_type'),
            item.get('col_category'),
            item.get('col_publish_time'),
            item.get('col_buyer_name'),
            item.get('col_projectId'),
            item.get('col_zone'),
            item.get('col_agent'),
            item.get('col_html_content'),
            item.get('index')
            ))

        else:pass
    def _handle_error(self, failue, item, spider):
        print "failue......",failue
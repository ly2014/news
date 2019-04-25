# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


class NewsPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456',
                                    db='news', charset='utf8')
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        sql = '''insert into news(title, publish_date) values('%s', '%s')''' % (item['title'], item['publish_date'])
        print(sql)
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            print(str(e))
        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()

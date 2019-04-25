import scrapy
import datetime
from news.items import NewsItem
import time
from news.util.langconv import *


class OldWeb(scrapy.spiders.Spider):
    name = 'old_spider'
    start_urls = ['http://www.takungpao.com']

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/73.0.3683.86 Safari/537.36'
    }

    handle_httpstatus_list = [404]

    def parse(self, response):
        now = datetime.datetime.now()
        year = now.year
        month = now.month
        day = now.day

        for i in range(2012, 2014):
            for j in range(1, 13):
                if i == 2013 and j > 5:
                    break
                for k in range(1, 32):
                    if i == 2013 and j == 5 and k > 25:
                        break
                    if i == year and j == month and k > day:
                        break
                    if i % 4 == 0:
                        if j == 2 and k > 29:
                            break
                    else:
                        if j == 2 and k > 28:
                            break
                    if j % 2 != 0 and k > 30:
                        break
                    y = str(i)
                    m = '0' + str(j) if j < 10 else str(j)
                    d = '0' + str(k) if k < 10 else str(k)
                    t = y + '-' + m + '-' + d
                    url = 'http://paper.takungpao.com/html/%s-%s/%s/index_%s.htm' % (y, m, d, t)
                    yield scrapy.Request(url=url, headers=self.headers, callback=self.parse1)
                    time.sleep(0.5)

    def parse1(self, response):
        dt = response.url
        dt = dt[dt.rfind('_') + 1:dt.rfind('.')]
        print(dt)
        items = response.xpath('//div[@id="none"]')
        for item in items:
            it = NewsItem()
            it['publish_date'] = dt
            title = item.xpath('text()').extract_first()
            title = Converter('zh-hans').convert(title)
            print(title)
            it['title'] = title
            yield it

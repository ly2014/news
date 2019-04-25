import scrapy
import datetime
from news.items import NewsItem
import time


class NewWeb(scrapy.spiders.Spider):
    name = 'new_spider'
    start_urls = ['http://www.takungpao.com']

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/73.0.3683.86 Safari/537.36'
    }

    handle_httpstatus_list = [404]

    count = 0

    def parse(self, response):
        now = datetime.datetime.now()
        year = now.year
        month = now.month
        day = now.day

        for i in range(2013, year + 1):
            if i > year:
                break
            for j in range(1, 13):
                if i == year and j > month:
                    break
                if i == 2013 and j < 5:
                    continue
                for k in range(1, 32):
                    if i == 2013 and j == 5 and k < 25:
                        continue
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
                    t = y + m + d
                    url = 'http://www.takungpao.com/paper/%s.html' % t
                    self.count += 1
                    yield scrapy.Request(url=url, headers=self.headers, callback=self.parse1)
                    time.sleep(0.5)

    def parse1(self, response):
        if response.status != 200:
            url = response.url.replace('www', 'news')
            print('==========================================>' + url)
            yield scrapy.Request(url=url, headers=self.headers, callback=self.parse1)
        dt = response.url
        dt = dt[dt.rfind('/') + 1:dt.rfind('.')]
        dt = dt[:4] + '-' + dt[4:6] + '-' + dt[6:]
        print(dt)
        items = response.xpath('//div[@class="pannel02"]//li')
        count = 0
        for item in items:
            it = NewsItem()
            it['publish_date'] = dt
            title = item.xpath('a/text()').extract_first()
            print(title)
            it['title'] = title
            count += 1
            if title.startswith('gw'):
                break
            yield it

import scrapy
import json
from scrapy.http import Request
from ..items  import DynamicSpiderItem
from bs4 import BeautifulSoup  # 解析网页
class DynamicSpider(scrapy.Spider):
    name = 'dynamicjson'
    allowed_domains = ["buff.163.com"]
    start_urls = [
        'https://buff.163.com/api/market/goods?game=csgo&page_num=1&page_size=80&category=weapon_ak47&sort_by=price.desc&min_price=100&max_price=200'
    ]

    def start_requests(self):
        headers = {
            'User-Agent': '',
            'Accept-Language': 'Accept-Language: zh-CN;q=0.5',
        }
        Cookies = {
            'session': '',
            'Device-Id': ' ',
            'csrf_token': '',
            'remember_me': ''
        }
        params ={
            'game': 'csgo',
            'min_price': 100,
            'max_price': 150,
            'page_num': 0,
            'page_size': 100
        }
        for url in self.start_urls:

            yield scrapy.Request(url=url, headers=headers, callback=self.parse,cookies=Cookies)

    def parse(self, response):
        goods = json.loads(response.body)
        for good in goods['data']['items']:
            filename = "data/buff.html"
            open(filename, 'a').write('\n1')
            open(filename, 'a').write(good['name'])
        yield good
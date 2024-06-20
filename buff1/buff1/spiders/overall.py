import json
import scrapy
from fake_useragent import UserAgent
from datetime import date
from ..items  import DynamicSpiderItem


import argparse

from bs4 import BeautifulSoup  # 解析网页
class Overall(scrapy.Spider):
    name = 'overall'

    allowed_domains = ["buff.163.com"]
    url = 'https://buff.163.com/api/market/goods'

    def __init__(self, category=None, *args, **kwargs):
        super(Overall, self).__init__(*args, **kwargs)
        self.category = category


    def paramadder(self,dict, url):
        p = '?'
        for key, value in dict.items():
            p += f"{key}={value}&"
        url += p
        url = url[:-1]
        return url

    ua = UserAgent()




    def start_requests(self):
        params = {'game': 'csgo',
                  'page_num': '1',
                  'page_size': '80',
                  'category': self.category,
                  'sort_by': 'price.desc'}
        url = 'https://buff.163.com/api/market/goods'
        start_urls = []
        for x in range(1, 7):
            p = params
            u = url
            p['page_num'] = str(x)
            u = self.paramadder(params, url)
            start_urls.append(u)

        headers = {
            'User-Agent': '',
            'Accept-Language': 'zh-CN',

        }
        Cookies = {
            'session': '1-hMB9idPY8IBTgeVYnGOEuRKp1JyGP8wahWzweR81x7Jd2042919270',
            'Device-Id': ' knYb3FE5srXqqaQw6Aky',
            'csrf_token': 'IjI2M2E1MjYyZWFlMTc4MzczOTcwYmE5MThlZmUxMzc0NmQxYTMxNjMi.GUvoYw.ADKGV5PNkaS-_bm1lnSpV4uJ4pk',
            'remember_me': 'U1091233342|KQ5cTOPKd2CAEWlUksvy4f8AjHip7LC2'
        }
        for url in start_urls:
            # url = self.paramadder(self.params, url)
            headers['User-Agent'] = self.ua.random

            yield scrapy.Request(url=url, headers=headers,cookies=Cookies ,callback=self.parse)


    def parse(self, response):
        item = DynamicSpiderItem()
        #item['title'] = response.xpath('//a/text()').get()
        #list = response.xpath('//h3')
        #title = response.xpath('//h3').get()
        body = response.body
        filename = "data/overall/"+self.category+'.csv'

        with open(filename,'a',encoding='utf-8') as file:
            data = json.loads(response.body.decode('utf-8'))

            property_names = [
                'id',
                'short_name',
                'quick_price',
            ]
            tags=[
                'category',#枪械型号AK-47
                'exterior',#磨损等级,崭新酒精
                'quality',#stattrak
                #'weapon'似乎和category相同
            ]
            for skin in data['data']['items']:#对每件皮肤
                try:
                    writebuffer = ''
                    for tag in tags:  # 加入tag级的属性
                        tagvalue = skin['goods_info']['info']['tags'][tag]['localized_name']
                        writebuffer += str(tagvalue) + ','
                    for property in property_names:#加入第一级的属性
                        p = property
                        propvalue= skin[property]
                        writebuffer += str(propvalue)+','
                    buffprice = float(skin['quick_price'])
                    steamprice = float(skin['goods_info']['steam_price_cny'])
                    ratio = round(steamprice/buffprice,2)
                    writebuffer += (str(steamprice))+','
                    writebuffer += str(ratio)+','
                    writebuffer += (str(date.today()))

                    # writebuffer = writebuffer[:-1]
                except KeyError as ke:
                    print("key error")
                    file.write('\n')
                file.write(writebuffer)
                file.write('\n')







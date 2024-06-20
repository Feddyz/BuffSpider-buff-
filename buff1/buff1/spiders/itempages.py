import json
import scrapy
from fake_useragent import UserAgent
from datetime import date

import pandas as pd

import argparse

from bs4 import BeautifulSoup  # 解析网页
class Overall(scrapy.Spider):
    name = 'itempages'

    allowed_domains = ["buff.163.com"]
    url = 'https://buff.163.com/api/market/goods'

    def __init__(self, category=None, *args, **kwargs):
        super(Overall, self).__init__(*args, **kwargs)
        # self.category = category

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
                  'category':'',
                  'sort_by': 'price.desc'}
        url = 'https://buff.163.com/api/market/goods'
        start_urls = []
        int_names = pd.read_csv('data/internal_name/weaponsbkp.csv',usecols=['internal_name'])

        for x in range(0, 65):

            p = params
            u = url
            p['category'] = int_names.loc[x]['internal_name']
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

        #item['title'] = response.xpath('//a/text()').get()
        #list = response.xpath('//h3')
        #title = response.xpath('//h3').get()
        body = response.body
        filename = 'data/internal_name/weapons.csv'

        with open(filename,'a',encoding='utf-8') as file:
            data = json.loads(response.body.decode('utf-8'))

            property_names = [
                #'id',
                #'internal_name',
                #'quick_price',
            ]
            tags=[
                'category',#枪械型号AK-47
                #'exterior',#磨损等级,崭新酒精
                #'quality',#stattrak
                #'weapon'似乎和category相同
            ]
            writebuffer = ''

            writebuffer += str(data['data']['items'][0]['goods_info']['info']['tags']['category']['internal_name'])+','
            writebuffer += str(data['data']['total_page'])
                # writebuffer = writebuffer[:-1]

            file.write(writebuffer)
            file.write('\n')







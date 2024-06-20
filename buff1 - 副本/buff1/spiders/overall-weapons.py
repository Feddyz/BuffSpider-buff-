import json
import random

import scrapy
from fake_useragent import UserAgent
from datetime import date
from ..items  import DynamicSpiderItem
import pandas as pd

import argparse

from bs4 import BeautifulSoup  # 解析网页
class Overallweapons(scrapy.Spider):
    def __init__(self, category=None, *args, **kwargs):
        super(Overallweapons, self).__init__(*args, **kwargs)
    name = 'overall-weapons'
    allowed_domains = ["buff.163.com"]
    url = 'https://buff.163.com/api/market/goods'
    def paramadder(self,dict, url):
        p = '?'
        for key, value in dict.items():
            p += f"{key}={value}&"
        url += p
        url = url[:-1]
        return url
    ua = UserAgent()

    def start_requests(self):

        cat_page = pd.read_csv('data/internal_name/weapons.csv',usecols=['internal_name','pages'])
        catlist = cat_page['internal_name']
        pages = cat_page['pages']
        datalen = len(catlist)
        for category in catlist:
            x = 1
            myth = 1718546644458
            params = {'game': 'csgo',
                      'page_num': '1',
                      'page_size': '80',
                      'category': category,
                      'sort_by': 'price.desc',
                      '_':'1718546644458'
                      }
            url = 'https://buff.163.com/api/market/goods'
            start_urls = []
            for x in range(1, pages.loc[x-1] + 1):
                p = params
                u = url
                p['page_num'] = str(x)
                myth += random.choice([1,2,3,4,5])
                p['_'] = myth
                u = self.paramadder(params, url)


                start_urls.append(u)
            headers = {
                'User-Agent': '',
                'Accept-Language': 'zh-CN',
                # 'Sec-Ch-Ua':'Google Chrome";v="125", "Chromium";v="125'
                'Sec-Ch-Ua-Mobile' : '?0',
                'Sec-Ch-Ua-Platform':'Windows',
                'Sec-Fetch-Dest':'empty',
                'Sec-Fetch-Mode':'cors',
                'Sec-Fetch-Site':'same-origin'
            }
            Cookies = {
                'session': '',
                'Device-Id': ' ',
                'csrf_token': '',
                'remember_me': ''
            }
            for url in start_urls:
                # url = self.paramadder(self.params, url)
                headers['User-Agent'] = self.ua.random

                yield scrapy.Request(url=url, headers=headers, cookies=Cookies, callback=self.parse)
            myth += 1000
            x+=1

    def parse(self, response):
        #item = DynamicSpiderItem()
        #item['title'] = response.xpath('//a/text()').get()
        #list = response.xpath('//h3')
        #title = response.xpath('//h3').get()
        body = response.body

        data = json.loads(response.body.decode('utf-8'))
        cat_name = data['data']['items'][0]['goods_info']['info']['tags']['category']['internal_name']
        filename = "data/overall/"+cat_name+'.csv'
        with open(filename,'a',encoding='utf-8') as file:


            property_names = [
                'id',
                'short_name',
                'sell_num',
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







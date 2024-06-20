import json
import random
import datetime
import scrapy
from fake_useragent import UserAgent
from datetime import date

import pandas as pd

import argparse

from bs4 import BeautifulSoup  # 解析网页
class buffhistory(scrapy.Spider):
    name = 'buffhistory'

    allowed_domains = ["buff.163.com"]
    url = 'https://buff.163.com/api/market/goods/price_history'

    def __init__(self, intname=None, *args, **kwargs):
        super(buffhistory, self).__init__(*args, **kwargs)
        self.intname = intname


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

        intended_id = pd.read_csv('data/id_list/'+self.intname+'.csv',header = None,names=['id'])
        self.id_list = intended_id['id']
        datalen = len(catlist)

        x = 1
        myth = 1718554632904


        self.params = {'game': 'csgo',
                  'goods_id':'',
                  'currency':'CNY',
                  'days':'30',
                  'with_sell_num':'false',
                  '_':'1718546644458',

                  }
        url = 'https://buff.163.com/api/market/goods/price_history'
        start_urls = []


        for x in self.id_list:
            p = self.params
            u = self.url
            self.params['goods_id'] = str(x)
            myth += random.choice([1,2,3,4,5])
            p['_'] = myth
            u = self.paramadder(self.params, url)


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
        count=-1
        for url in start_urls:
            # url = self.paramadder(self.params, url)
            count+=1
            headers['User-Agent'] = self.ua.random

            yield scrapy.Request(url=url, headers=headers, cookies=Cookies, callback=self.parse,
                                 meta = {'id':self.id_list[count]})
        myth += 100
        x+=1



    def parse(self, response):
        # item = DynamicSpiderItem()
        # item['title'] = response.xpath('//a/text()').get()
        # list = response.xpath('//h3')
        # title = response.xpath('//h3').get()
        body = response.body

        data = json.loads(response.body.decode('utf-8'))

        filename = "data/buffpricehistory/"+self.intname+'.csv'
        id_meta = response.request.meta['id']
        print(id_meta)
        with open(filename,'a',encoding='utf-8') as file:

            for record in data['data']['price_history']:#对每件皮肤
                writebuffer =''
                try:
                    price = record[1]
                    # 毫秒级时间戳
                    writebuffer += str(price)+','

                    timestamp_ms = record[0]
                    # 将毫秒转换为秒，并减去1970年1月1日以来的秒数
                    seconds = timestamp_ms / 1000.0
                    # 使用datetime模块计算日期和时间
                    dt = datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=seconds)
                    formatted_dt = dt.strftime('%Y%m%d%H')
                    writebuffer+= str(formatted_dt)+','
                    writebuffer += str(id_meta)

                    # writebuffer = writebuffer[:-1]
                except KeyError as ke:
                    print("key error")
                    file.write('\n')
                file.write(writebuffer)
                file.write('\n')

        df = pd.read_csv(filename,header = None,names = ['price','time','id'])

        # 去除重复的行
        df_unique = df.drop_duplicates()

        # 将去重后的数据保存到新的CSV文件
        df_unique.to_csv(filename, index=False)
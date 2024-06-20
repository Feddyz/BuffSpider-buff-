import json
import scrapy
from fake_useragent import UserAgent
from datetime import date
from ..items  import DynamicSpiderItem
import fake_useragent   # 导入库_Dep\python3.11\Lib\site-packages\fake_useragent

from bs4 import BeautifulSoup  # 解析网页
class allitems(scrapy.Spider):
    ua = UserAgent()
    name = 'allitems.csv'
    allowed_domains = ["buff.163.com"]
    url = 'https://buff.163.com/api/market/goods'


    def paramadder(dict,url):
        p = '?'
        for key,value  in dict.items():
            p+=f"{key}={value}&"
        url += p
        url = url[:-1]
        return url


    params = {
        'game':'csgo',
        'page_num':'1',
        'page_size':'80',
        #'category':'weapon_ak47',
        #'min_price': '100',
        #'max_price': '150'
        'tab':'selling',
        'sort_by':'price.desc'
    }

    start_urls = []
    for x in [59,144,157,158]:
        p = params
        u = url
        p['page_num'] = str(x)
        u = paramadder(params, url)
        start_urls.append(u)
    print("hello")
    print('url='+url)
    headers = {
        'User-Agent': '',
        'Accept-Language': 'zh-CN',

    }
    Cookies = {
        'session': '1-hMB9idPY8IBTgeVYnGOEuRKp1JyGP8wahWzweR81x7Jd2042919270',
        'Device-Id': ' knYb3FE5srXqqaQw6Aky',
        'csrf_token': 'IjI2M2E1MjYyZWFlMTc4MzczOTcwYmE5MThlZmUxMzc0NmQxYTMxNjMi.GUvoYw.ADKGV5PNkaS-_bm1lnSpV4uJ4pk',
        'remember_me':'U1091233342|KQ5cTOPKd2CAEWlUksvy4f8AjHip7LC2'
    }

    def start_requests(self):

        for url in self.start_urls:
            # url = self.paramadder(self.params, url)
            self.headers['User-Agent'] = self.ua.random
            yield scrapy.Request(url=url, headers=self.headers,cookies=self.Cookies ,callback=self.parse)


    def parse(self, response):
        item = DynamicSpiderItem()
        #item['title'] = response.xpath('//a/text()').get()
        #list = response.xpath('//h3')
        #title = response.xpath('//h3').get()
        body = response.body
        filename = "data/allitems.csv"

        with open(filename,'a',encoding='utf-8') as file:
            data = json.loads(response.body.decode('utf-8'))

            property_names = [
                'id',
                'short_name',
                #'quick_price',
            ]
            """tags=[
                'category',#枪械型号AK-47,
                'exterior',#磨损等级,崭新酒精
                'quality',#stattrak
                # 'weapon' 似乎和category相同
            ]"""
            for skin in data['data']['items']:#对每件皮肤
                try:
                    writebuffer = ''
                    """for tag in tags:  # 加入tag级的属性
                        tagvalue = skin['goods_info']['info']['tags'][tag]['localized_name']
                        writebuffer += str(tagvalue) + ','"""
                    for property in property_names:#加入第一级的属性
                        p = property
                        propvalue= skin[property]
                        writebuffer += str(propvalue)+','
                    internal_name = skin['goods_info']['info']['tags']['category']['internal_name']
                    writebuffer+= str(internal_name)
                    # writebuffer = writebuffer[:-1]

                    file.write(writebuffer)
                    file.write('\n')
                except KeyError as e:
                    print("error key")
                    writebuffer = ''

                    for property in property_names:  # 加入第一级的属性
                        p = property
                        propvalue = skin[property]
                        writebuffer += str(propvalue) + ','

                    writebuffer += str(internal_name)
                    # writebuffer = writebuffer[:-1]

                    file.write(writebuffer+"wrong internal name")
                    file.write('\n')







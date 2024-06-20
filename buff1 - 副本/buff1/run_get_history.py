from scrapy.cmdline import execute
import pandas as pd
import subprocess
"""读取data/gethistory.csv文件中作为internal_name,并根据internal_name从data/id_list中获取对应internal_name的id列表发送历史价格查询
    读取data/gethistory.csv文件
    读取data/gethistory.csv文件
    读取data/gethistory.csv文件

"""
intended_category = pd.read_csv('data/gethistory.csv',names = ['internal_names'],header = None)
cat_list = intended_category['internal_names']
for category in cat_list:
    execute(['scrapy', 'crawl', 'buffhistory','-a','intname='+category])
print('end')
from scrapy.cmdline import execute

# 本程序为爬虫起始入口，直接运行本程序即可运行爬虫
# execute(['scrapy', 'crawl', 'overall' , '-a','category=weapon_ak47' ,'-o','output.json'])



execute(['scrapy', 'crawl', 'overall-weapons']) #自动根据data/internal_name/weapons.csv爬取所有item的overall，
#execute(['scrapy', 'crawl', 'buffhistory','-a','intname=weapon_zeus'])# 测试取得电
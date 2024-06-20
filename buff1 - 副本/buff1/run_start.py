from scrapy.cmdline import execute

# 本程序为爬虫起始入口，直接运行本程序即可运行爬虫
execute(['scrapy', 'crawl', 'overall' , '-a','category=weapon_ak47' ,'-o','output.json'])



#execute(['scrapy', 'crawl', 'overall-weapons'])
#execute(['scrapy', 'crawl', 'buffhistory','-a','intname=weapon_zeus'])# 测试取得电击枪所有的皮肤历史价格 慎用
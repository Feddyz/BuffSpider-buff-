import scrapy


class BuffSpider(scrapy.Spider):
    name = "buff"
    allowed_domains = ["buff.163.com"]
    start_urls = ["https://buff.163.com/"]

    def parse(self, response):
        filename = "buff.html"
        
        open(filename,'w').write(str(response.body))
        pass

from scrapy.http import HtmlResponse
from selenium import webdriver
from scrapy import signals

class SeleniumMiddleware:
    def __init__(self):
        self.driver = None

    @classmethod
    def from_crawler(cls, crawler):
        middleware = cls()
        crawler.signals.connect(middleware.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(middleware.spider_closed, signal=signals.spider_closed)
        return middleware

    def open_browser(self):
        if not self.driver:
            self.driver = webdriver.Chrome()

    def process_request(self, request, spider):
        if not self.driver:
            self.open_browser()

        self.driver.get(request.url)
        self.driver.add_cookie({'name': 'session_id', 'value': 'your_session_id'})
        # 如果需要设置cookie，这里应该有相应的代码
        # 例如：self.driver.add_cookie({'name': 'session_id', 'value': 'your_session_id'})

        # 刷新页面以应用cookie（如果需要）
        # self.driver.refresh()

        # 获取页面内容并返回给 Scrapy
        body = self.driver.page_source
        return HtmlResponse(url=request.url, body=body, request=request, encoding='utf-8')

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

    def spider_closed(self, spider):
        if self.driver:
            self.driver.quit()
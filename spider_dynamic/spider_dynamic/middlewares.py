# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
from scrapy.http import HtmlResponse
from scrapy import signals
import time
from fake_useragent import FakeUserAgent

class SpiderDynamicSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class SpiderDynamicDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        pass

    #  对页面响应体数据的篡改, 如果是每个模块的 url 请求, 则处理完数据并进行封装
    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        """
        three parameters
        :param request: 响应对象所对应的请求对象
        :param response: 拦截到的响应对象
        :param spider: 爬虫文件中对应的爬虫类的实例对象，可以通过这个参数拿到NetbaseSpider中的一些属性或方法
        :return:
        """
        if request.url in ["http://news.163.com/domestic/","http://war.163.com/","http://news.163.com/world/","http://news.163.com/air/"]:
            spider.browser.get(url=request.url)
            #more_btn = spider.browser.find_element_by_class_name("post_addmore")    #更多按钮
            #print(more_btn)
            js = "window.scrollTo(0,document.body.scrollHeight)"
            spider.browser.execute_script(js)
            # if more_btn and request.url == "http://news.163.com/domestic/":
            # more_btn.click()
            time.sleep(1)  # 等待加载,  可以用显示等待来优化.
            row_response = spider.browser.page_source
            return HtmlResponse(url=spider.browser.current_url, body=row_response, encoding="utf8",
                                request=request)  # 参数url指当前浏览器访问的url(通过current_url方法获取), 在这里参数url也可以用request.url
            # 参数body指要封装成符合HTTP协议的源数据, 后两个参数可有可无
        else:
            return response  # 是原来的主页的响应对象

    # 请求出错了的操作, 比如ip被封了,可以在这里设置ip代理
    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        return None

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

class RandomUserAgent(object):
    def __init__(self):
        self.ua = FakeUserAgent()
        self.num = 0
        self.useragent = ""

    def process_request(self, request, spider):
        self.num += 1
        if self.num % 20 == 0:
            self.useragent = self.ua.data_randomize
        request.headers['User_Agent'] = self.useragent
        #request.meta['proxy'] = ""    代理设置
        #print(self.useragent)
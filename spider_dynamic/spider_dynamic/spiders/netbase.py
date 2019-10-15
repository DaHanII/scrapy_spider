# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from ..items import SpiderDynamicItem

#无头浏览器设置
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")

class NetbaseSpider(scrapy.Spider):
    name = 'netbase'
    #allowed_domains = ['news.163.com']
    start_urls = ['http://news.163.com/']

    #实例化一个浏览器对象
    def __init__(self):
        self.browser = webdriver.Chrome(executable_path='D:\工作\chromedriver.exe', chrome_options=chrome_options)
        super().__init__()

    def start_requests(self):
        url = "https://news.163.com/"
        yield Request(url, callback=self.parse_index)

    #爬虫结束后关闭浏览器
    def close(self, spider):
        self.browser.quit()

    # 访问主页的url, 拿到对应板块的response
    def parse_index(self, response):
        div_list = response.xpath("//div[@class='ns_area list']/ul/li/a/@href").extract()
        index_list = [3,4,6,7]
        for index in index_list:
            response = scrapy.Request(div_list[index],callback=self.parse_detail)
            yield response

    # 对每一个板块进行详细访问并解析, 获取板块内的每条新闻的url
    def parse_detail(self,response):
        div_res = response.xpath("//div[@class='data_row news_article clearfix ']")
        # print(len(div_res))
        title = div_res.xpath(".//div[@class='news_title']/h3/a/text()").extract_first()
        pic_url = div_res.xpath("./a/img/@src").extract_first()
        detail_url = div_res.xpath("//div[@class='news_title']/h3/a/@href").extract_first()
        infos = div_res.xpath(".//div[@class='news_tag//text()']").extract()
        info_list = []
        for info in infos:
            info = info.strip()
            info_list.append(info)
        info_str = "".join(info_list)
        item = SpiderDynamicItem()

        item["title"] = title
        item["detail_url"] = detail_url
        item["pic_url"] = pic_url
        item["info_str"] = info_str

        yield scrapy.Request(url=detail_url,callback=self.parse_content,meta={"item":item})    # 通过 参数meta 可以将item参数传递进 callback回调函数,再由 response.meta[...]取出来

    # 对每条新闻的url进行访问, 并解析
    def parse_content(self,response):
        item = response.meta["item"]    # 获取从response回调函数由meta传过来的 item 值
        content_list = response.xpath("//div[@class='post_text']/p/text()").extract()
        content = "".join(content_list)
        item["content"] = content
        yield item

# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
from ..items import SplashExamplesItem
from scrapy.loader import ItemLoader
from scrapy import Request

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/js']

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, args={'images': 0, 'timeout': 5})

    def parse(self, response):
        for sel in response.xpath("//div[@class='quote']"):
            quote = sel.xpath('span[@class="text"]/text()').extract()[0]
            author = sel.xpath('span/small[@class="author"]/text()').extract()[0]
            yield {'quote': quote, 'author': author}
        href = response.xpath('//li[@class="next"]/a/@href').extract()
        if href:
            url = response.urljoin(href[0])
            yield SplashRequest(url, args={'images': 0, 'timeout': 5})


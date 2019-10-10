# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import re
from ..items import SpiderDoubanItem
from scrapy.loader import ItemLoader

class DbspiderSpider(scrapy.Spider):
    name = 'dbspider'
    #allowed_domains = ['douban.com']
    start_urls = ['https://movie.douban.com/top250']

    def parse(self, response):
        lista = response.xpath('//div[@class="hd"]/a')
        for a in lista:
            href = a.xpath('@href').extract()[0]
            mvname = a.xpath('span[1]/text()').extract()[0]
            #print(mvname)
            dinfo = {'mvname': mvname}
            yield Request(href, meta = dinfo, callback = self.details_parse)
        nexturl = response.xpath('//link[@rel = "next"]/@href').extract()
        baseurl = 'https://movie.douban.com/top250'
        if nexturl:
            nexturl = nexturl[0]
            req_url = baseurl + nexturl
            yield Request(req_url, callback = self.parse)

    def getInfoByRe(self, instr, restr):
        m = re.search(restr, instr, re.S)
        if m:
            info = m.groups()[0]
        else:
            info = ""
        return info

    def details_parse(self,response):
        dinfo = response.meta
        item1 = ItemLoader(item = SpiderDoubanItem(), response = response)
        item1.add_value('mMvName', dinfo['mvname'])
        item1.add_xpath('mDirectors', '//a[@rel = "v:directedBy"]/text()')
        item1.add_xpath('mActors', '//a[@rel = "v:starring"]/text()')
        item1.add_xpath('mType', '//span[@property = "v:genre"]/text()')
        #directors = response.xpath('//a[@rel = "v:directedBy"]/text()').extract()
        #item['mDirectors'] = ' '.join(directors)   #去掉中括号
        #actors = response.xpath('//a[@rel = "v:starring"]/text()').extract()
        #mvtype = response.xpath('//span[@property = "v:genre"]/text()').extract()
        #item['mType'] = mvtype
        showplace = self.getInfoByRe(response.text, r'制片国家/地区:</span>(.+?)<br/>')
        item1.add_value('mShowplace', showplace)
        #item['mShowplace'] = showplace
        language = self.getInfoByRe(response.text, r'语言:</span>(.+?)<br/>')
        item1.add_value('mLanguage', language)
        #item['mLanguage'] = language
        mvnames = self.getInfoByRe(response.text, r'又名:</span>(.+?)<br/>')
        item1.add_value('mMvnames', mvnames)
        #item['mMvnames'] = mvnames
        item1.add_xpath('mShowtime', '//span[@property = "v:initialReleaseDate"]/text()')
        item1.add_xpath('mMvruntime', '//span[@property = "v:runtime"]/text()')
        item1.add_xpath('mScore', '//strong[@property = "v:average"]/text()')
        item1.add_xpath('mVote', '//span[@property = "v:votes"]/text()')
        #mvshowtime = response.xpath('//span[@property = "v:initialReleaseDate"]/text()').extract()
        #item['mShowtime'] = mvshowtime
        #mvruntime = response.xpath('//span[@property = "v:runtime"]/text()').extract()
        #item['mMvruntime'] = mvruntime
        #print(directors,actors,mvtype,showplace,language,mvnames,mvshowtime,mvruntime)
        return item1.load_item()
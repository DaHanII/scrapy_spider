# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, Compose, Join

def mysplit(info):
    return info.split('/')

class SpiderDoubanItem(scrapy.Item):
    # define the fields for your item here like:
    mMvName = scrapy.Field(input_processor=MapCompose(mysplit, str.strip), output_processor=Join('/'))
    mDirectors = scrapy.Field(input_processor=MapCompose(mysplit, str.strip), output_processor=Join('/'))
    mActors = scrapy.Field(input_processor=MapCompose(mysplit, str.strip), output_processor=Join('/'))
    mType = scrapy.Field(input_processor=MapCompose(mysplit, str.strip), output_processor=Join('/'))
    mShowplace = scrapy.Field(input_processor=MapCompose(mysplit, str.strip), output_processor=Join('/'))
    mLanguage = scrapy.Field(input_processor=MapCompose(mysplit, str.strip), output_processor=Join('/'))
    mMvnames = scrapy.Field(input_processor=MapCompose(mysplit, str.strip), output_processor=Join('/'))
    mShowtime = scrapy.Field(input_processor=MapCompose(mysplit, str.strip), output_processor=Join('/'))
    mMvruntime = scrapy.Field(input_processor=MapCompose(mysplit, str.strip), output_processor=Join('/'))
    mScore = scrapy.Field(input_processor=MapCompose(mysplit, str.strip), output_processor=Join('/'))
    mVote = scrapy.Field(input_processor=MapCompose(mysplit, str.strip), output_processor=Join('/'))
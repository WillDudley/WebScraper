# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose


def to_int(string):
    return int(string.replace(',', ''))


def strip(string):
    return string.strip()


class PetitionsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    text = scrapy.Field()
    votes = scrapy.Field(output_processor=MapCompose(to_int))
    status = scrapy.Field()
    url = scrapy.Field()
    more_detail = scrapy.Field()
    gov_response = scrapy.Field()#output_processor=MapCompose(arr_to_str))
    deadline = scrapy.Field(output_processor=MapCompose(strip))
    last_updated = scrapy.Field(serializer=str)

# -*- coding: utf-8 -*-
import scrapy
from quotes.items import QuotesItem
from scrapy.loader import ItemLoader


class QuotesScraperSpider(scrapy.Spider):
    name = 'quotes_scraper'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        for selector in response.xpath("//div[@class='quote']"):

            item = QuotesItem()
            l = ItemLoader(item=item, selector=selector)
            l.add_xpath('text', "*[@class='text']/text()")
            l.add_xpath('author', ".//*[@class='author']/text()")
            l.add_xpath('tags', "*/a[@class='tag']/text()")

            l.load_item()

            url = response.urljoin(response.xpath(".//a/@href").extract_first())
            yield scrapy.Request(url=url, callback=self.parse_author, meta={'item': item}, dont_filter=True)

            # yield l.load_item()


    def parse_author(self, response):
        next_l = ItemLoader(item=response.meta['item'], response=response)
        next_l.add_xpath('author_dob', "//span[@class='author-born-date']/text()")
        next_l.add_xpath('author_birth_city', "//*[@class='author-born-location']/text()")
        next_l.add_xpath('author_birth_country', "//*[@class='author-born-location']/text()")
        return next_l.load_item()


# import scrapy
# from quotes.items import QuotesItem
#
#
# class QuotesScraperSpider(scrapy.Spider):
#     name = 'quotes_scraper'
#     allowed_domains = ['quotes.toscrape.com']
#     start_urls = ['http://quotes.toscrape.com/']
#
#     def parse(self, response):
#         for selector in response.xpath("//div[@class='quote']"):
#
#             item = QuotesItem()
#             item['text'] = selector.xpath("*[@class='text']/text()").extract_first()
#             item['author'] = selector.xpath(".//*[@class='author']/text()").extract_first()
#             item['tags'] = selector.xpath("*/a[@class='tag']/text()").extract_first()
#
#             url = response.urljoin(response.xpath(".//a/@href").extract_first())
#             yield scrapy.Request(url=url, callback=self.parse_author, meta={'item': item}, dont_filter=True)
#
#
#     def parse_author(self, response):
#         item = response.meta['item']
#         item['author_birth_city'] = 'foo'
#         return item

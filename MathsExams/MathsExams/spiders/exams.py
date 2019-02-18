# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from MathsExams.items import MathsexamsItem

class ExamsSpider(scrapy.Spider):

    http_user = '###############'
    http_pass = '###############'
    name = 'exams'
    allowed_domains = ['exampapers.cf.ac.uk/cgi-bin/papers.pl?dcode=maths']
    start_urls = ['http://exampapers.cf.ac.uk/cgi-bin/papers.pl?dcode=maths/']
    pages = [f'{j}{i:02d}' for i in range(8,19) for j in ['a','b']] + ['r09', 'r18']

    def parse(self, response):

        for url_suffix in self.pages:


        if self.pages[self.index] is not None:
        print(response.xpath("//div[@class='body']"))
        print("********************************************************")
        print(response.xpath("//a[starts-with(@href,'/cgi-bin')]/text()"))
        print("********************************************************")

        yield {
            'text': response.xpath("/*")
        }


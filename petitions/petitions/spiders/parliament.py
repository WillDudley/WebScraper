# -*- coding: utf-8 -*-
# import scrapy
#
#
# class ParliamentSpider(scrapy.Spider):
#     name = 'parliament'
#     allowed_domains = ['petition.parliament.uk']
#     start_urls = ['https://petition.parliament.uk/petitions/']
#
#     def parse(self, response):
#         page = 'main_page'
#         filename = page
#         with open(filename, 'w') as f:
#             petitions = response.xpath("//*[contains(@class, 'petition-item')]")
#             for petition in petitions:
#                 petition_description = petition.xpath('*/a/text()')[0]
#                 # f.write(petition_description + "\n")
#                 yield {
#                     'text': petition_description.extract_first()
#                 }


# import scrapy
#
#
# class ParliamentSpider(scrapy.Spider):
#     name = 'parliament'
#     root_url = 'https://petition.parliament.uk'
#
#     allowed_domains = ['petition.parliament.uk']
#     start_urls = [f'{root_url}/petitions/']
#
#     def __init__(self):
#         self.petition_text = None
#         self.votes = None
#         self.status = None
#         self.gov_response = None
#         self.author = None
#
#     def parse_details(self, response):
#         self.author = response.xpath('//li[@class="meta-created-by"]/text()').extract()
#
#     def parse(self, response):
#         petitions = response.xpath("//*[contains(@class, 'petition-item')]")
#         for petition in petitions:
#             petition_url = petition.xpath("*/a")
#
#             self.petition_text = petition_url.xpath("text()").extract_first()
#             self.votes = int(petition.xpath("*/span[@class='count']/text()").extract_first().replace(',', ''))
#             self.status = 'Open' if 'petition-open' in petition.attrib['class'] else 'Closed'
#
#             if self.votes >= 10000:
#                 more_detail_url = f'{self.root_url}{petition_url}'
#                 response.follow(more_detail_url, callback=self.parse_details)
#
#             yield {
#                 'text': self.petition_text,
#                 'votes': self.votes,
#                 'status': self.status,
#                 'author': self.author,
#                 'gov_response': self.gov_response
#             }
#
#         next_page = response.xpath('//a[@class="next"]/@href').extract_first()
#         if next_page is not None:
#             yield response.follow(next_page, callback=self.parse)


import scrapy
from scrapy.loader import ItemLoader
from petitions.items import PetitionsItem


class ParliamentSpider(scrapy.Spider):
    name = 'parliament'
    root_domain = 'petition.parliament.uk'

    allowed_domains = [root_domain]
    start_urls = [f'https://{root_domain}/petitions/']

    def parse(self, response):
        for selector in response.xpath("//*[contains(@class, 'petition-item')]"):

            status = 'Open' if 'petition-open' in selector.attrib['class'] else 'Closed'

            url = response.urljoin(selector.xpath("*/a/@href").extract_first())

            item = PetitionsItem()
            l = ItemLoader(item=item, selector=selector)
            l.add_xpath('text', "*/a/text()")
            l.add_value('status', status)
            l.add_xpath('votes', "*/span[@class='count']/text()")
            l.add_value('url', url)

            l.load_item()

            # if item['votes'][0] >= 10000:
                # l.add_value('gov_response', 'passed')
            yield scrapy.Request(url, callback=self.parse_detail, meta={'item': item}, dont_filter=True)

            next_page = response.xpath('//a[@class="next"]/@href').extract_first()

            if next_page is not None:
                yield response.follow(next_page, callback=self.parse)



    def parse_detail(self, response):
        l = ItemLoader(item=response.meta['item'], response=response)
        l.add_xpath('more_detail', "//main[@id='content']/div[1]//*/text()")
        l.add_xpath('gov_response', "//section[@id='response-threshold']/blockquote[@class='pull-quote']/p/text()")
        l.add_xpath('deadline', "//li[@class='meta-deadline']/text()|//ul[@class='petition-meta']/li[not(@class='meta-created-by')]/text()")

        return l.load_item()



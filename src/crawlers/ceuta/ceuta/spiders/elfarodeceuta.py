# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ceuta.loaders import el_faro_de_ceuta_loader


class ElfarodeceutaSpider(CrawlSpider):
    name = 'elfarodeceuta'
    allowed_domains = ['elfarodeceuta.es']
    start_urls = ['https://elfarodeceuta.es/']
    custom_settings = {
        'RABBITMQ_QUEUE': 'elfarodeceuta',
    }
    rules = (
        Rule(LinkExtractor(allow=r''), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        if response.xpath('//div[@class="content-inner"]'):
            return el_faro_de_ceuta_loader(response)
        else:
            return {}

# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ceuta.loaders import el_pueblo_de_ceuta_loader


class ElpueblodeceutaSpider(CrawlSpider):
    name = 'elpueblodeceuta'
    allowed_domains = ['elpueblodeceuta.es']
    start_urls = ['http://elpueblodeceuta.es/']
    custom_settings = {
        'RABBITMQ_QUEUE': 'elpueblodeceuta',
    }

    rules = (
        Rule(LinkExtractor(allow=r'/sec/.*'), follow=True),
        Rule(LinkExtractor(allow=r'\w+/\d+/\w+'), callback='parse_item',
             follow=True),
        Rule(LinkExtractor(allow=r'.*'), follow=True),
    )

    def parse_item(self, response):
        return el_pueblo_de_ceuta_loader(response)

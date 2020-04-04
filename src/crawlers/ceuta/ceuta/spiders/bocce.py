# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ceuta.loaders import bocce_loader


class BocceSpider(CrawlSpider):
    name = 'bocce'
    allowed_domains = ['ceuta.es']
    start_urls = ['http://www.ceuta.es/ceuta/bocce']
    custom_settings = {
        'RABBITMQ_QUEUE': 'bocce',
    }

    rules = (
        Rule(LinkExtractor(
            allow=r'/ceuta/component/jdownloads/viewcategory/\d+-\d+\?Itemid=\d+'),
            follow=True),
        Rule(LinkExtractor(
            allow=r'/ceuta/component/jdownloads/viewcategory/\d+-\w+\?Itemid=\d+'),
            follow=True),
        Rule(LinkExtractor(
            allow=r'/ceuta/component/jdownloads/finish/\d+-.*/.*\?Itemid=\d+'),
            callback='parse_pdf')
    )

    def parse_pdf(self, response):
        file_path = '{}/{}/{}.pdf'.format(
            self.settings.get('FILE_FOLDER'),
            self.name,
            response.url.split('/')[-1].split('?')[0])

        return bocce_loader(response, file_path, self.name)

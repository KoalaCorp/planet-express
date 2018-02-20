# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BocceSpider(CrawlSpider):
    name = 'bocce'
    allowed_domains = ['ceuta.es']
    start_urls = ['http://www.ceuta.es/ceuta/bocce']

    rules = (
        Rule(
            LinkExtractor(
                allow=r'/ceuta/component/jdownloads/viewcategory/\d+-\d+\?Itemid=\d+'),
                follow=True),
        Rule(
            LinkExtractor(
                allow=r'/ceuta/component/jdownloads/viewcategory/\d+-\w+\?Itemid=\d+'),
                follow=True),
        Rule(
            LinkExtractor(
                allow=r'http://www.ceuta.es/ceuta/component/jdownloads/finish/\d+-.*/.*\?Itemid=\d+')
            )
    )

    def parse_pdf(self, response):
        i = {}

        pdf_file = open(self.settings.get('FILE_FOLDER')+'/'+self.name+'/'+response.url.split('/')[-1].split('?')[0]+'.pdf', 'wb')
        pdf_file.write(response.body)
        pdf_file.close()

        return i

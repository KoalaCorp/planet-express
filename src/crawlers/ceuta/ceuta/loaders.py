import logging

from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Join

from ceuta.items import ElPuebloDeCeutaItem, ElFaroDeCeutaItem, BocceItem


logger = logging.getLogger()


def bocce_loader(response, file_path, name):
    bocce = BocceItem()
    bocce['url'] = response.url
    bocce['file_path'] = file_path

    pdf_file = open(file_path, 'wb')
    pdf_file.write(response.body)
    pdf_file.close()

    logger.info('{} file downloaded: {}'.format(
        name, file_path))

    return bocce


class ElPuebloDeCeutaLoader(ItemLoader):
    default_output_processor = TakeFirst()
    content_out = Join()


def el_pueblo_de_ceuta_loader(response):
    item = ElPuebloDeCeutaLoader(
        item=ElPuebloDeCeutaItem(),
        response=response)
    item.add_value('url', response.url)
    item.add_xpath('autor', '//div[@class="firma"]/text()')
    item.add_xpath('date_time', '//span[@class="date"]/text()')
    item.add_xpath('title', '//h1[@class="new_title"]/text()')
    item.add_xpath('content', '//div[@class="new_text "]/p/text()')
    return item.load_item()


class ElFaroDeCeutaLoader(ItemLoader):
    default_output_processor = TakeFirst()
    content_out = Join()


def el_faro_de_ceuta_loader(response):
    item = ElFaroDeCeutaLoader(
        item=ElFaroDeCeutaItem(),
        response=response)
    item.add_value('url', response.url)
    item.add_xpath('autor', '//div[@class="jeg_meta_autor"]/a/text()')
    item.add_xpath('date_time', '//div[@class="jeg_meta_date"]/a/text()')
    item.add_xpath('title', '//div[@class="entry-header"]/h1/text()')
    item.add_xpath('content',
                   '//div[@class="content-inner"]/node()/text()')
    return item.load_item()

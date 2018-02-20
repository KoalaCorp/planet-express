from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Join

from ceuta.items import ElPuebloDeCeutaItem

class ElPuebloDeCeutaLoader(ItemLoader):
    default_output_processor = TakeFirst()
    content_out = Join()

def el_pueblo_de_ceuta_loader(response):
    item = ElPuebloDeCeutaLoader(
        item=ElPuebloDeCeutaItem(),
        response=response)
    item.add_value('url', response.url)
    item.add_xpath('autor', '//div[@class="firma"]/text()')
    item.add_xpath('date_time', '//div[@class="fecha"]/text()')
    item.add_xpath('title', '//div[@class="NOTICIA"]/h1/text()')
    item.add_xpath('content', '//div[@class="TEXTO_PARRAFO "]/p/text()')
    return item.load_item()

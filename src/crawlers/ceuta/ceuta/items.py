# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
from scrapy import Item, Field


class BaseItem(Item):
    url = Field()
    scraped = Field()
    updated = Field()


class BocceItem(BaseItem):
    url = Field()
    file_path = Field()
    content = Field()


class CeutaItem(BaseItem):
    autor = Field()
    date_time = Field()
    title = Field()
    content = Field()


class ElPuebloDeCeutaItem(CeutaItem):
    pass


class ElFaroDeCeutaItem(CeutaItem):
    pass

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhnoverlItem(scrapy.Item):
    # define the fields for your item here like:
    book_name = scrapy.Field()
    book_author = scrapy.Field()
    book_nums = scrapy.Field()
    book_type = scrapy.Field()
    book_brief = scrapy.Field()
    book_url = scrapy.Field()
    all_catalog = scrapy.Field()
    pass

class ZhnoverlItemCatalogInfo(scrapy.Item):
    chather_title=scrapy.Field()
    chather_url=scrapy.Field()
    all_catalog=scrapy.Field()

class ZhnoverlItemChatherContent(scrapy.Item):
    chather_content=scrapy.Field()
    chather_url=scrapy.Field()


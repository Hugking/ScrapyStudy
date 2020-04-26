# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class IpItem(scrapy.Item):
    # define the fields for your item here like:
    ip = scrapy.Field()
    port_img_urls = scrapy.Field()
    city = scrapy.Field()

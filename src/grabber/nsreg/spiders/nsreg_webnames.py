# -*- coding: utf-8 -*-
import scrapy

from ..base_site_spider import BaseSpiderComponent, EMPTY_PRICE, find_price
from ..items import NsregItem

REGEX_PATTERN = r"([0-9]+)[.,\s]?₽.*"


class NsregWebnamesSpider(scrapy.Spider):
    name = "nsreg_webnames"
    allowed_domains = ["webnames.ru"]
    start_urls = ["https://www.webnames.ru/tld/catalog/ru"]
    site_names = ("ООО «Регтайм»",)

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.component = BaseSpiderComponent(
            start_urls=self.start_urls,
            allowed_domains=self.allowed_domains,
            site_names=self.site_names,
            regex=REGEX_PATTERN,
            path={
                'price_reg': '/html/body/section[1]/div[4]/div[1]/div[2]/div/table/tbody/tr[1]/td[2]/strong/span/text()',
                'price_prolong': '/html/body/section[1]/div[4]/div[1]/div[2]/div/table/tbody/tr[3]/td[2]/strong/span/text()',
                'price_change': '/html/body/div[2]/div/div[2]/div[1]/div/div/div[1]/div[2]/span/text()'
            }
        )

    def parse_price_change(self, response):
        price_change = response.xpath(self.component.path['price_change']).get()
        price_change = find_price(self.component.regex['price_change'], price_change)

        item = NsregItem()
        item['name'] = "ООО «Регтайм»"
        price = item.get('price', EMPTY_PRICE)
        price['price_change'] = price_change
        item['price'] = price

        yield item

    def parse(self, response):

        price_reg = response.xpath(self.component.path['price_reg']).get()
        price_reg = find_price(self.component.regex['price_reg'], price_reg)

        price_prolong = response.xpath(self.component.path['price_prolong']).get()
        price_prolong = find_price(self.component.regex['price_prolong'], price_prolong)

        yield scrapy.Request('https://www.webnames.ru/domains/transfer', callback=self.parse_price_change)

        item = NsregItem()
        item['name'] = "ООО «Регтайм»"
        price = item.get('price', EMPTY_PRICE)
        price['price_reg'] = price_reg
        price['price_prolong'] = price_prolong
        item['price'] = price

        return item

# -*- coding: utf-8 -*-
import scrapy

from ..base_site_spider import BaseSpiderComponent


class NsregFlexbeSpider(scrapy.Spider):
    name = "nsreg_flexbe.py"
    start_urls = ["https://flexbe.ru/domains/"]
    allowed_domains = ("flexbe.ru")
    site_names = ("ООО «Флексби»",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.component = BaseSpiderComponent(
            start_urls=self.start_urls,
            allowed_domains=self.allowed_domains,
            site_names=self.site_names,
            regex=r"([0-9]+)[.,\s]?₽.*",
            path={
                'price_reg': '/html/body/main/section[2]/div[2]/div[3]/div/div/div[2]/div/div/div/table/tbody/tr[1]/td[2]/text()',
                'price_prolong': '/html/body/main/section[2]/div[2]/div[3]/div/div/div[2]/div/div/div/table/tbody/tr[1]/td[3]/text()',
                'price_change': '/html/body/main/section[2]/div[2]/div[3]/div/div/div[3]/div/div/div/table/tbody/tr[1]/td[2]/text()'
            }
        )

    def parse(self, response):
        return self.component.parse(response)

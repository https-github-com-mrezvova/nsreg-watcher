# -*- coding: utf-8 -*-
import scrapy
from ..base_site_spider import BaseSpiderComponent


class NsregCentralregSpider(scrapy.Spider):

    name = "nsreg_centralreg_ru"
    start_urls = ["https://centralreg.ru/tarify-i-oplata/"]
    allowed_domains = ("centralreg.ru",)
    site_names = ("ООО «Перспектива»",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.component = BaseSpiderComponent(
            start_urls=self.start_urls,
            allowed_domains=self.allowed_domains,
            site_names=self.site_names,
            regex=r"\s{3}([0-9]{2,3})",
            path={
                'price_reg': '/html/body/div[3]/div[2]/div/div/article/div/div/div[2]/div/div[2]/div/div/div/div/table/tbody/tr[3]/td[2]/div/div/div/text()',
                'price_prolong': '/html/body/div[3]/div[2]/div/div/article/div/div/div[2]/div/div[2]/div/div/div/div/table/tbody/tr[4]/td[2]/div/div/div/text()',
                'price_change': '/html/body/div[3]/div[2]/div/div/article/div/div/div[2]/div/div[2]/div/div/div/div/table/tbody/tr[7]/td[2]/div/div/div/text()'
                }
            )

    def parse(self, response):
        return self.component.parse(response)

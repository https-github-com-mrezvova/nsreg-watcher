# -*- coding: utf-8 -*-
import scrapy

from ..base_site_spider import BaseSpiderComponent


class NsregElastichostingSpider(scrapy.Spider):
    name = "nsreg_elastichosting"
    start_urls = ["https://my.elastichosting.ru/domain/pricing?currency=3"]
    allowed_domains = ("elastichosting.ru")
    site_names = ("ООО «ЭластикХостинг»",)

    # Конструктор класса
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Инициализация компонента BaseSpiderComponent с требуемыми параметрами
        self.component = BaseSpiderComponent(
            start_urls=self.start_urls,
            allowed_domains=self.allowed_domains,
            site_names=self.site_names,
            regex=r"₽\s*([0-9]+\.[0-9]+)\s*RUB",
            path={
                'price_reg': '//tr[.//strong[.=".ru"]]/td[contains(.//span, "Новая цена")]/text()[preceding-sibling::span[contains(@class, "tld-label")]]',
                'price_prolong': '//tr[.//strong[.=".ru"]]/td[contains(.//span, "Продление")]/text()[preceding-sibling::span[contains(@class, "tld-label")]]',
                'price_change': '//tr[.//strong[.=".ru"]]/td[contains(.//span, "Передача")]/text()[preceding-sibling::span[contains(@class, "tld-label")]]'
            }
        )

    def parse(self, response):
        return self.component.parse(response)

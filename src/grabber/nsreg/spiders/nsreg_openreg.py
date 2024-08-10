import scrapy

from ..base_site_spider import BaseSpiderComponent


class MultiSiteSpider4(scrapy.Spider):
    name = 'nsreg_openreg'
    start_urls = ('http://openreg.ru/',)
    allowed_domains = ('openreg.ru',)
    site_names = ('ООО «НФ МЕДИА»',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.component = BaseSpiderComponent(
            start_urls=self.start_urls,
            allowed_domains=self.allowed_domains,
            site_names=self.site_names,
            regex=r"([0-9]+)\s+₽.*",
            path={
                'price_reg': (
                    '/html/body/div[1]/div/div/div/main/article/div/div/div[4]/div/div/div[5]/div/div/div/div/table/tbody/tr[1]/td[2]/div/p/text()'
                ),
                'price_prolong': (
                    '/html/body/div[1]/div/div/div/main/article/div/div/div[4]/div/div/div[5]/div/div/div/div/table/tbody/tr[2]/td[2]/div/p/text()'
                ),
                'price_change': (
                    '/html/body/div[1]/div/div/div/main/article/div/div/div[4]/div/div/div[5]/div/div/div/div/table/tbody/tr[3]/td[2]/div/p/text()'
                )
            }
        )

    def parse(self, response):
        return self.component.parse(response)

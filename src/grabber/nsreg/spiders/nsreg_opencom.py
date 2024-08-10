import scrapy

from ..base_site_spider import BaseSpiderComponent


class MultiSiteSpider4(scrapy.Spider):
    name = 'nsreg_opencom'
    start_urls = ('https://opencom.ru/',)
    allowed_domains = ('opencom.ru',)
    site_names = ('ООО «Открытые коммуникации»',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.component = BaseSpiderComponent(
            start_urls=self.start_urls,
            allowed_domains=self.allowed_domains,
            site_names=self.site_names,
            regex=r"([0-9]+)₽.*",
            path={
                'price_reg': 'translate(/html/body/div[1]/div/main/div/div/div/article/div/div/section[3]/div/div/div/div[3]/div/table/tbody/tr[3]/td[2]/p/text(), " ", "")',
                'price_prolong': 'translate(/html/body/div[1]/div/main/div/div/div/article/div/div/section[3]/div/div/div/div[3]/div/table/tbody/tr[4]/td[2]/p/text(), " ", "")',
                'price_change': 'translate(/html/body/div[1]/div/main/div/div/div/article/div/div/section[3]/div/div/div/div[3]/div/table/tbody/tr[5]/td[2]/p/text(), " ", "")',
            },
        )

    def parse(self, response):
        return self.component.parse(response)

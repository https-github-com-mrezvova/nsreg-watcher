"""
Namebit перенесен в отдельный спайдер из-за того,
что в multi_site_spider3 не работает xpath для этого конкретного сайта
"""
import scrapy

from ..base_site_spider import BaseSpiderComponent


class NsregNamebitSpider(scrapy.Spider):
    name = 'nsreg_namebit'
    allowed_domains = ['namebit.ru']
    start_urls = ['https://namebit.ru/#features-2']
    site_names = ('ООО «НЕЙМБИТ»',)
    custom_settings = {
        'CONCURRENT_ITEMS': 0,
        'DOWNLOAD_DELAY': 1.25,
        'RANDOMIZE_DOWNLOAD_DELAY': False,
        'RETRY_TIMES': 3,
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64; rv:7.0.1) Gecko/20100101 Firefox/7.7'
    }

    # Конструктор класса
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Инициализация компонента BaseSpiderComponent с требуемыми параметрами
        self.component = BaseSpiderComponent(
            start_urls=self.start_urls,
            allowed_domains=self.allowed_domains,
            site_names=self.site_names,
            regex=r".*?(\d+).*",
            path={
                'price_reg': (
                    'translate(/html/body/div[1]/div[2]/div/div/div[1]/div/div/div/div[1]/div/div/div[2]/div/p[1]/text(), " ", "")'
                ),
                'price_prolong': (
                    'translate(/html/body/div[1]/div[2]/div/div/div[1]/div/div/div/div[2]/div/div/div[2]/div/p[1]/text(), " ", "")'
                ),
                'price_change': (
                    'translate(/html/body/div[1]/div[2]/div/div/div[1]/div/div/div/div[3]/div/div/div[2]/div/p[1]/text(), " ", "")'
                )
            }

        )

    # Метод для обработки ответов на запросы
    def parse(self, response):
        # Применение метода parse компонента BaseSpiderComponent
        return self.component.parse(response)

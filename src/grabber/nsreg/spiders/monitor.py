import scrapy

from catalog.models import ParseHistory, Registrator


def has_data_changed(company, data):
    """Проверяет, изменились ли данные для компании."""
    for field, value in data.items():
        if getattr(company, field) != value:
            return True
    return False


class NSRegSpider(scrapy.Spider):
    name = "monitor"
    allowed_domains = ['cctld.ru']
    start_urls = ['https://cctld.ru/domains/reg/']

    def __init__(self, name=None, **kwargs):
        ParseHistory.objects.create()

    def parse(self, response):
        for reg in response.xpath('//*[@id="registrator-list"]/div/div'):
            data = {
                'name': reg.xpath('div/span[1]/span[1]/span/text()').get(),
                'nic_handle1': reg.xpath('div/span[1]/span[2]/span[1]/text()').get(),
                'nic_handle2': reg.xpath('div/span[1]/span[2]/span[2]/text()').get(),
                'city': reg.xpath('div/span[2]/text()').get(),
                'website': reg.xpath('div/a/@href').get()
            }

            company, created = Registrator.objects.get_or_create(name=data['name'])

            # Проверка, изменились ли данные
            if created or has_data_changed(company, data):
                for field, value in data.items():
                    setattr(company, field, value)
                company.save()

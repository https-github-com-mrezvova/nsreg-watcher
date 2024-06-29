# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from catalog.models import ParseHistory, Price, Registrator


class NsregPipeline:

    def process_item(self, item, spider):
        price = item.get(
            "price",
            {
                "price_reg": None,
                "price_prolong": None,
                "price_change": None,
            },
        )

        Price.objects.create(
            price_reg=price["price_reg"],
            price_change=price["price_change"],
            price_prolong=price["price_prolong"],
            parse=ParseHistory.objects.order_by("-id").all()[0],
            domain="ru",
            registrator=Registrator.objects.get(name=item.get("name")),
        )

        spider.logger.info(f'Saving item {item.get("name")}')
        return item

    def close_spider(self, spider):
        pass

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from main_page.models import Product


class Store77Pipeline:
    def process_item(self, item, spider):
        print("Received item:", item)
        product = Product(
            name=item['name'],
            price=item['price'],
            specifies=item['specifies'],
            link=item['link'],
            image_link=item['image_link'],
            seller=item['seller'],
            market_place=item['market_place'],
        )
        product.save()
        return item

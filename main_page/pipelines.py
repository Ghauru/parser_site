from .models import Product


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

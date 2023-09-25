import re
import sqlite3
import scrapy
from scrapy_splash import SplashRequest
from main_page.models import Product


def product_to_database(product):
    product.name = product.name.replace('\"', '')
    product.specifies = product.specifies.replace('\"', '')
    sql_insert_query = f'INSERT INTO main_page_product(name, link, price, specifies, seller,' \
                       f' image_link, search_name, market_place' \
                       f') VALUES("{product.name}",' \
                       f' "{product.link}", "{product.price}", "{product.specifies}",' \
                       f' "{product.seller}", "{product.image_link}"' \
                       f',"{product.search_name}", "{product.market_place}")'
    db_path = 'C://Users//rules//PycharmProjects//pythonProject2//db.sqlite3'
    with sqlite3.connect(db_path) as db:
        cursor = db.cursor()
        cursor.execute(sql_insert_query)
        db.commit()
        cursor.close()


class CitilinkSpider(scrapy.Spider):
    name = "citilink"

    def __init__(self, url=None, search_name=None, *args, **kwargs):
        super().__init__(**kwargs)
        self.url = url
        self.search_name = search_name

    def start_requests(self):
        yield SplashRequest(self.url, callback=self.parse,
                            endpoint='render.html',
                            args={'wait': 5},
                            meta={'search_name': self.search_name}
                            )

    def parse(self, response):
        try:
            page_count = response.css('li.ui-pager__page._clickable button::text').getall()[-1]
        except:
            page_count = 1
        for i in range(1, int(page_count)+1):
            page_url = self.url + f'&page={i}'
            yield SplashRequest(page_url, callback=self.parse_page, endpoint='render.html',
                                args={'wait': 5})  # Задержка 5 секунд для загрузки AJAX-контента

    def parse_page(self, response):
        item_link = response.css('.block-offer-item > a')
        for link in item_link:
            href = 'https://e2e4online.ru' + link.css("::attr(href)").get()
            yield SplashRequest(href, callback=self.parse_item, meta={'url': href, 'search_name': self.search_name},
                                args={'wait': 5})  # Задержка 5 секунд для загрузки AJAX-контента

    def parse_item(self, response):
        name = response.css('.offer-card-new__title::text').get()
        price = response.css('.price-block__price._WAIT span::text').get()
        if price is None:
            price = response.css('.price-block__price._IN_PLACE span::text').get()
        price = int(re.sub(r"\D", "", price))
        container = response.css('.offer-properties-new')
        text = container.xpath('.//text()').getall()
        specifies = ''
        for i in range(1, len(text), 2):
            if i+1 < len(text):
                specifies += text[i] + ': ' + text[i+1] + ', '
            else:
                specifies += text[i]
        link = response.url
        search_name = response.meta['search_name']
        image_link = response.css('div.image-item__picture-wrapper img').attrib['src']
        seller = 'e2e4online'
        market_place = 'e2e4online'
        product = Product(name=name, price=price, specifies=specifies, link=link, image_link=image_link, seller=seller,
                          market_place=market_place, search_name=search_name)
        product_to_database(product)


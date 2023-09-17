import sqlite3
from main_page.models import Product
import scrapy
from scrapy_splash import SplashRequest
import re


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


class Store77Spider(scrapy.Spider):
    name = "store77"

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
        page_count = response.css('.pagination')[0]
        last_li_value = page_count.css('li:nth-last-child(2) a::text').get()
        for i in range(1, int(last_li_value)+1):
            page_url = self.url + f'&PAGEN_1={i}'
            yield SplashRequest(page_url, callback=self.parse_page, endpoint='render.html',
                                args={'wait': 5})  # Задержка 5 секунд для загрузки AJAX-контента

    def parse_page(self, response):
        product_links = response.css(".blocks_product_fix_w > a")
        for link in product_links:
            href = 'https://store77.net' + link.css("::attr(href)").get()
            yield SplashRequest(href, callback=self.parse_product, meta={'url': href, 'search_name': self.search_name},
                                args={'wait': 5})

    def parse_product(self, response):

        name = response.css(".title_card_product::text").get()
        price = response.css(".price_title_product::text").get().replace(' ', '')
        price = int(price.replace('Р', ''))
        table_rows = response.css('table.tabs_table tr')
        specifies = []
        for row in table_rows:
            row_text = row.css('td::text').getall()
            row_text = [text.strip() for text in row_text if text.strip()]
            text = 'доставки'
            if len(row_text) > 1:
                text = ' '.join(row_text)
            elif len(row_text) == 1:
                text = row_text[0]
            if 'доставки' not in text.lower() and 'наличие' not in text.lower():
                specifies.append(text)
        specifies = list(set(specifies))
        specifies = '\n'.join(specifies)
        link = response.meta['url']
        search_name = response.meta['search_name']
        image_link = response.css('div#cardPhoto a.swiper-slide::attr(style)').extract()[0]
        image_link = re.findall(r"'(.*?)'", image_link)
        image_link = image_link[0]
        seller = 'store77'
        market_place = 'store77'
        product = Product(name=name, price=price, specifies=specifies, link=link, image_link=image_link, seller=seller,
                          market_place=market_place, search_name=search_name)
        product_to_database(product)


import scrapy
from scrapy_djangoitem import DjangoItem
from main_page.models import Product


class StoreParserItem(DjangoItem):
    django_model = Product


import json
import os
import sys
import django
from scrapy.crawler import CrawlerProcess
from store_parser.store_parser.spiders.store77 import Store77Spider
from main_page.models import Product


def main_parse(url):
    # Установите настройки Django
    search_name = url
    url = 'https://store77.net/search/?q=' + '%20'.join(url.split()) + '&ms=1'
    sys.path.append('C://Users//rules//PycharmProjects//pythonProject2')
    os.environ['DJANGO_SETTINGS_MODULE'] = 'parser_site.settings'
    django.setup()

    # Создайте экземпляр паука Scrapy

    # Создайте экземпляр процесса Scrapy Crawler
    process = CrawlerProcess(settings={
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'FEED_FORMAT': 'json',
        'FEED_URI': 'C://Users//rules//PycharmProjects//pythonProject2//output.json',
    })

    # Запустите процесс Crawler с использованием паука
    process.crawl(Store77Spider, u=url)
    process.start()
    process.join()

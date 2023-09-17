from store_parser.spiders.store77 import Store77Spider
import scrapydo


def main_parse(url):
    # Установите настройки Django
    search_name = url.lower()
    url = 'https://store77.net/search/?q=' + '%20'.join(url.split()) + '&ms=1'
    spider_cls = Store77Spider
    scrapydo.run_spider(spider_cls, url=url, search_name=search_name)

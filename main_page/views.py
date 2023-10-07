import threading
import os

from django.shortcuts import render
from .models import Product
from .scrapy_integration import main_parse, second_parse, jpg_parse
import scrapydo

scrapydo.setup()
lock = threading.Lock()


def main_page(request):
    file_path = 'C://Users//rules//PycharmProjects//pythonProject2//staticfiles//pictures//image.jpg'

    if os.path.exists(file_path):
        os.remove(file_path)
    return render(request, 'main_page/home.html')


def search_view(request):
    query = request.GET.get('query')
    try:
        product = Product.objects.filter(search_name__icontains=query.lower(), market_place='store77')[0]
        jpg_parse(product.image_link)
    except IndexError:
        main_parse(query)
        product = Product.objects.filter(search_name__icontains=query.lower(), market_place='store77')[0]
        jpg_parse(product.image_link)
    try:
        item = Product.objects.filter(search_name__icontains=query.lower(), market_place='e2e4online')[0]
    except IndexError:
        second_parse(query)
        item = Product.objects.filter(search_name__icontains=query.lower(), market_place='e2e4online')[0]

    return render(request, 'main_page/home.html', {'product': product, 'item': item})

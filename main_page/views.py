import threading

from django.shortcuts import render
from .models import Product
from .scrapy_integration import main_parse
import scrapydo

scrapydo.setup()
lock = threading.Lock()


def main_page(request):
    return render(request, 'main_page/home.html')


def search_view(request):
    query = request.GET.get('query')
    try:
        product = Product.objects.filter(search_name__icontains=query.lower(), market_place='store77')[0]
    except IndexError:
        main_parse(query)
        product = Product.objects.filter(search_name__icontains=query.lower(), market_place='store77')[0]

    return render(request, 'main_page/home.html', {'product': product})

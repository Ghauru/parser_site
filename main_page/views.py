from django.shortcuts import render
from .models import Product
from .scrapy_integration import main_parse
import scrapydo
from django.http import HttpResponse


scrapydo.setup()


def main_page(request):
    return render(request, 'main_page/home.html')


def search_view(request):
    query = request.GET.get('query')
    print('---------------------------------------------------------------------------------------------')
    print(query)
    print('---------------------------------------------------------------------------------------------')
    try:
        product = Product.objects.filter(search_name__icontains=query, market_place='store_77')[0]
    except:

        main_parse(query)
        product = Product.objects.filter(search_name__icontains=query, market_place='store_77')[0]

    return render(request, 'main_page/home.html', {'product': product})

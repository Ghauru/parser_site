import threading
import os

from django.http import FileResponse
from django.shortcuts import render
from .models import Product
from .scrapy_integration import main_parse, second_parse, jpg_parse
import scrapydo

scrapydo.setup()
lock = threading.Lock()


def main_page(request):
    image_available = False
    return render(request, 'main_page/home.html', {'image_available': image_available})


def search_view(request):
    image_available = True
    query = request.GET.get('query')
    try:
        product = Product.objects.filter(search_name__icontains=query.lower(), market_place='store77')[0]
        jpg_parse(product.image_link)
        folder_path = 'C:/Users/rules/PycharmProjects/pythonProject2/media/full/'
        file_names = os.listdir(folder_path)
        if len(file_names) == 1:
            file_path = os.path.join(folder_path, file_names[0])

    except IndexError:
        main_parse(query)
        product = Product.objects.filter(search_name__icontains=query.lower(), market_place='store77')[0]
        jpg_parse(product.image_link)
        folder_path = 'C:/Users/rules/PycharmProjects/pythonProject2/media/full/'
        file_names = os.listdir(folder_path)
        if len(file_names) == 1:
            file_path = os.path.join(folder_path, file_names[0])
    try:
        item = Product.objects.filter(search_name__icontains=query.lower(), market_place='e2e4online')[0]
    except IndexError:
        second_parse(query)
        item = Product.objects.filter(search_name__icontains=query.lower(), market_place='e2e4online')[0]

    return render(request, 'main_page/home.html', {'product': product, 'item': item,
                                                   'image_available': image_available, 'image_path': file_path})


def download_file1(request):
    file_path = 'C://Users//rules//PycharmProjects//pythonProject2//main_page//static//files//file1.csv'  # Путь к первому файлу
    response = FileResponse(open(file_path, 'rb'), as_attachment=True)
    return response


def download_file2(request):
    file_path = 'C://Users//rules//PycharmProjects//pythonProject2//main_page//static//files//file2.csv'  # Путь ко второму файлу
    response = FileResponse(open(file_path, 'rb'), as_attachment=True)
    return response

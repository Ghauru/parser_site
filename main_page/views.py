from django.shortcuts import render
from django.http import HttpResponse


def main_page(request):
    return HttpResponse('<h1>Главная</h1>')
from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('search', views.search_view, name='search_view'),
    path('download/file1/', views.download_file1, name='download_file1'),
    path('download/file2/', views.download_file2, name='download_file2'),
]

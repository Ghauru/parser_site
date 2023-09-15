from django.db import models


class Product(models.Model):
    class Meta:
        ordering = ['name', 'price']

    name = models.CharField(max_length=100)
    price = models.IntegerField()
    specifies = models.TextField()
    link = models.CharField(max_length=255)
    image_link = models.CharField(max_length=255)
    seller = models.CharField(max_length=100)
    market_place = models.CharField(max_length=20)
    search_name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Market(models.Model):
    name = models.CharField(max_length=50)
    link = models.CharField(max_length=255)

    def __str__(self):
        return self.name

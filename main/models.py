from django.db import models
from django.contrib.auth.models import User

class Categories(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='category', null=True, blank=True)

    def __str__(self):
        return self.name


class Banners(models.Model):
    title = models.CharField(max_length=50)
    text = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='banners')

    def __str__(self):
        return self.title

class Products(models.Model):
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    discount = models.IntegerField(null=True, blank=True)
    description = models.TextField()
    photo = models.ImageField(upload_to='products')

    def __str__(self):
        return self.name

class Shop(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    total = models.IntegerField(default=0)
    status = models.IntegerField(default=0)

    def __str__(self):
        return str(self.id)

class ShopItems(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    total = models.IntegerField()

    def __str__(self):
        return str(self.id)
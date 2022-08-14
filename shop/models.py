import datetime

from django.db import models, transaction
from requests import request

from ecommerce_api.settings import AUTH_USER_MODEL


class Category(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=30)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class ImageProduct(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    upload = models.ImageField(upload_to='products/')
    product = models.ForeignKey('shop.Product', on_delete=models.CASCADE, related_name='images', null=False)


class Product(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    category = models.ForeignKey('shop.Category', on_delete=models.CASCADE, related_name='products')
    price = models.FloatField()
    stock = models.IntegerField()
    active = models.BooleanField(default=True)


class Order(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    product = models.ForeignKey('shop.Product', on_delete=models.SET_NULL, null=True, related_name='orders')
    cart = models.ForeignKey('shop.Cart', on_delete=models.CASCADE, related_name='orders')
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)


class Cart(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')
    ordered = models.BooleanField(default=False)
    ordered_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.user.usename + self.id

    @transaction.atomic
    def make_ordered(self):
        if self.ordered:
            return
        self.ordered = True
        self.ordered_date = datetime.datetime.now()
        self.orders.update(ordered=True)
        self.save()

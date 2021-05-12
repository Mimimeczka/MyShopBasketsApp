from django.db import models


class Product(models.Model):
    product_id = models.IntegerField()
    quantity = models.IntegerField()


class Basket(models.Model):
    date = models.DateField()
    products = models.ForeignKey(Product, on_delete=models.CASCADE)
    sum = models.DecimalField(max_digits=10, decimal_places=2)

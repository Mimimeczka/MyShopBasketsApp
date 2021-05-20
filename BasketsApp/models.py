from django.db import models


class Basket(models.Model):
    date = models.DateField()
    sum = models.DecimalField(max_digits=10, decimal_places=2)
    user_id = models.IntegerField(default=None)
    summarized = models.BooleanField(default=False)

    def __str__(self):
        return f'Basket ({self.date}), summarized: {self.summarized}'


class Product(models.Model):
    product_id = models.IntegerField()
    quantity = models.IntegerField()
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, default=None, null=True, related_name='products')


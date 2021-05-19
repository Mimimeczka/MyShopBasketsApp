from .models import Basket, Product
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['product_id', 'quantity', 'id']


class BasketSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Basket
        fields = ['date', 'id', 'sum', 'user_id', 'products']
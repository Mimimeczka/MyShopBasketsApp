from .models import Basket
from rest_framework import serializers


class BasketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Basket
        fields = ['date', 'products', 'sum', 'user_id']
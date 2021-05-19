from .serializers import BasketSerializer
from rest_framework import viewsets
from .models import Basket, Product
from rest_framework.response import Response
from datetime import date
import requests
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404


class BasketViewSet(viewsets.ModelViewSet):
    serializer_class = BasketSerializer

    def get_queryset(self):
        basket = Basket.objects.all()
        return basket

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        response = requests.get('http://127.0.0.1:8001/api/products/1/')
        product = response.json()
        print(product['price'])
        serializer = BasketSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = BasketSerializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        basket = Basket.objects.create(
            date=date.isoformat(date.today()),
            sum=0,
            user_id=request.query_params['user_id']
        )
        serializer = BasketSerializer(basket, many=False)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        return Response('Cannot update basket')

    def destroy(self, request, *args, **kwargs):
        return Response('Cannot delete basket')


@api_view(['POST'])
def add_product_to_basket(request, basket_id, product_id):

    basket = get_object_or_404(Basket, id=basket_id)
    response = requests.get(f'http://127.0.0.1:8001/api/products/{product_id}/')
    product_from_response = response.json()
    quantity = request.data['quantity']

    basket_response = requests.get(f'http://127.0.0.1:8002/api/baskets/{basket_id}/')
    product_in_basket = basket_response.json()

    for product in product_in_basket['products']:
        if product['product_id'] == product_id:
            product_to_update = Product.objects.get(id=product['id'])
            to_add = int(product_to_update.quantity) + int(quantity)
            product_to_update.quantity = int(to_add)
            product_to_update.save()

        else:
            Product.objects.create(
                product_id=int(product_from_response['id']),
                quantity=int(quantity),
                basket=basket
            )

    previous_sum_basket = float(basket.sum)
    products_sum = float(quantity) * float(product_from_response['price'])
    actual_sum_basket = previous_sum_basket + products_sum
    basket.sum = actual_sum_basket
    basket.save()

    # serializer = BasketSerializer(basket, many=True)
    return Response(f'Product {product_from_response} add to basket')


@api_view(['POST'])
def delete_product_from_basket(request, basket_id, product_id):

    basket = get_object_or_404(Basket, id=basket_id)
    response = requests.get(f'http://127.0.0.1:8001/api/products/{product_id}/')
    product_from_response = response.json()
    quantity = request.data['quantity']

    basket_response = requests.get(f'http://127.0.0.1:8002/api/baskets/{basket_id}/')
    product_in_basket = basket_response.json()

    for product in product_in_basket['products']:
        if product['product_id'] == product_id:
            product_to_update = Product.objects.get(id=product['id'])
            to_update = int(product_to_update.quantity) - int(quantity)
            if to_update > 0:
                product_to_update.quantity = int(to_update)
                product_to_update.save()
            elif to_update < 0:
                raise ValueError('Cannot remove more product than you have')
            else:
                product_to_update.delete()

    previous_sum_basket = float(basket.sum)
    products_sum = float(quantity) * float(product_from_response['price'])
    actual_sum_basket = previous_sum_basket - products_sum
    basket.sum = actual_sum_basket
    basket.save()

    # serializer = BasketSerializer(queryset, many=True)
    return Response(f'działa url basket: {basket}, product: {product}, suma: {basket.sum}')



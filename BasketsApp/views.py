from .serializers import BasketSerializer
from rest_framework import viewsets
from .models import Basket, Product
from rest_framework.response import Response
from datetime import date
import requests
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from .validators import validator_check_basket_is_summarized, validator_check_content_basket
from rest_framework import status


class BasketViewSet(viewsets.ModelViewSet):
    serializer_class = BasketSerializer

    def get_queryset(self):
        basket = Basket.objects.all()
        return basket

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
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


def change_basket_value(basket, quantity, product_from_response, operation):
    previous_sum_basket = float(basket.sum)
    products_sum = float(quantity) * float(product_from_response['price'])
    if operation == 'add':
        actual_sum_basket = previous_sum_basket + products_sum
    elif operation == 'delete':
        actual_sum_basket = previous_sum_basket - products_sum
    else:
        return Response('Wrong action', status=status.HTTP_401_UNAUTHORIZED)
    basket.sum = actual_sum_basket
    basket.save()
    return basket


@api_view(['POST'])
def add_product_to_basket(request, basket_id, product_id):

    basket = get_object_or_404(Basket, id=basket_id)
    validator_check_basket_is_summarized(basket)
    response = requests.get(f'http://127.0.0.1:8001/api/products/{product_id}/')
    if response.status_code == 404:
        return Response('Product not found', status=status.HTTP_404_NOT_FOUND)

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
            break

    else:
        Product.objects.create(
            product_id=int(product_from_response['id']),
            quantity=int(quantity),
            basket=basket
        )

    change_basket_value(basket, quantity, product_from_response, 'add')

    serializer = BasketSerializer(basket, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def delete_product_from_basket(request, basket_id, product_id):

    basket = get_object_or_404(Basket, id=basket_id)
    validator_check_basket_is_summarized(basket)
    response = requests.get(f'http://127.0.0.1:8001/api/products/{product_id}/')
    product_from_response = response.json()
    quantity = request.data['quantity']

    basket_response = requests.get(f'http://127.0.0.1:8002/api/baskets/{basket_id}/')
    product_in_basket = basket_response.json()

    access = False

    for product in product_in_basket['products']:
        if product['product_id'] == product_id:
            access = True
            product_to_update = Product.objects.get(id=product['id'])
            to_update = int(product_to_update.quantity) - int(quantity)
            if to_update > 0:
                product_to_update.quantity = int(to_update)
                product_to_update.save()
            elif to_update < 0:
                return Response('Cannot remove more product than you have', status=status.HTTP_401_UNAUTHORIZED)
            elif to_update == 0:
                product_to_update.delete()
            else:
                return Response('Wrong value', status=status.HTTP_401_UNAUTHORIZED)
            break

    if not access:
        return Response('Cannot remove product which is not in the basket', status=status.HTTP_401_UNAUTHORIZED)

    change_basket_value(basket, quantity, product_from_response, 'delete')

    serializer = BasketSerializer(basket, many=False)
    return Response(serializer.data)


def change_product_value(product_id, quantity):
    product_response = requests.get(f'http://127.0.0.1:8001/api/products/{product_id}/')
    my_product = product_response.json()
    update_product_quantity = my_product['quantity'] - quantity

    if update_product_quantity < 0:
        raise Exception(f"You can not buy this product quantity ({my_product['name']}). Available quantity is: {my_product['quantity']}")

    requests.put(f'http://127.0.0.1:8001/api/products/{product_id}/', data={
        'name': '',
        'description': '',
        'price': '',
        'quantity': update_product_quantity
    })


@api_view(['GET'])
def summarize_basket(request, basket_id):
    basket = get_object_or_404(Basket, id=basket_id)
    validator_check_basket_is_summarized(basket)
    validator_check_content_basket(basket_id)

    basket_response = requests.get(f'http://127.0.0.1:8002/api/baskets/{basket_id}/')
    product_in_basket = basket_response.json()
    for product in product_in_basket['products']:
        change_product_value(product['product_id'], product['quantity'])

    basket.summarized = True
    basket.save()
    requests.post(f'http://127.0.0.1:8002/api/baskets/?user_id={basket.user_id}')

    serializer = BasketSerializer(basket, many=False)
    return Response(serializer.data)



from django.core.exceptions import ValidationError
import requests


def validator_check_basket_is_summarized(basket):
    if basket.summarized:
        raise ValidationError('Cannot modify summarized basket')


def validator_check_content_basket(basket_id):
    basket_response = requests.get(f'http://127.0.0.1:8002/api/baskets/{basket_id}/')
    product_in_basket = basket_response.json()
    if not product_in_basket['products']:
        raise ValidationError('Cannot summarize empty basket')



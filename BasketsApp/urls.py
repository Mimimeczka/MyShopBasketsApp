from django.urls import path, include
from rest_framework import routers
from BasketsApp import views

router = routers.DefaultRouter()
router.register(r'baskets', views.BasketViewSet, basename='Basket')

urlpatterns = [
    path('', include(router.urls)),
    path('baskets/<int:basket_id>/add/<int:product_id>/', views.add_product_to_basket, name='add_product_to_basket'),
    path('baskets/<int:basket_id>/delete/<int:product_id>/', views.delete_product_from_basket, name='delete_product_from_basket'),
]

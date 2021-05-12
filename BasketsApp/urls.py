from django.urls import path, include
from rest_framework import routers
from BasketsApp import views

router = routers.DefaultRouter()
router.register(r'baskets', views.BasketViewSet, basename='Basket')

urlpatterns = [
    path('', include(router.urls))
]
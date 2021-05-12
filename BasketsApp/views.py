from .serializers import BasketSerializer
from rest_framework import viewsets
from .models import Basket
from rest_framework.response import Response
from datetime import date


class BasketViewSet(viewsets.ModelViewSet):
    # queryset = Product.objects.all()
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
            products=None,
            sum=0,
            user_id=request.query_params['user_id']
        )
        serializer = BasketSerializer(basket, many=False)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        return Response('Cannot update basket')

    def destroy(self, request, *args, **kwargs):
        return Response('Cannot delete basket')
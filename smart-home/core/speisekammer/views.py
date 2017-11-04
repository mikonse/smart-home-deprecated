from django.shortcuts import get_object_or_404
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.response import Response

from .models import Product, ProductInstance, ShoppingList
from .serializers import ProductSerializer, InstanceSerializer, ItemCountSerializer, ShoppingListSerializer


class ProductList(GenericAPIView, ListModelMixin, CreateModelMixin):
    serializer_class = ProductSerializer

    def get_queryset(self):
        if 'filter' in self.request.query_params:
            return Product.objects.filter(name__contains=self.request.query_params['filter'])
        else:
            return Product.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ProductDetail(GenericAPIView, RetrieveModelMixin, DestroyModelMixin):
    serializer_class = ProductSerializer
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'

    def get_object(self):
        return get_object_or_404(Product, pk=self.kwargs['pk'])

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        if 'stock_io' in request.data:
            self.get_object().stock_io(request.data['stock_io'])
            return Response(self.get_object())
        else:
            return Response({
                'error': 'Please specify a stock_io parameter to modify the stock count'
            })

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ProductInstanceList(GenericAPIView, ListModelMixin, CreateModelMixin):
    serializer_class = InstanceSerializer

    def get_queryset(self):
        return ProductInstance.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ProductInstanceDetail(GenericAPIView, RetrieveModelMixin, DestroyModelMixin):
    serializer_class = InstanceSerializer
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'

    def get_object(self):
        return get_object_or_404(ProductInstance, pk=self.kwargs['pk'])

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ProductItemCount(GenericAPIView):
    serializer_class = ItemCountSerializer

    def get_object(self):
        return get_object_or_404(ProductInstance, pk=self.kwargs['pk'])

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.stock_io(1)
        serializer = self.serializer_class(instance)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.stock_io(-1)
        serializer = self.serializer_class(instance)
        return Response(serializer.data)


class ShoppingLists(GenericAPIView, ListModelMixin, CreateModelMixin):
    serializer_class = ShoppingListSerializer

    def get_queryset(self):
        return ShoppingList.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ShoppingListDetail(GenericAPIView, RetrieveModelMixin, DestroyModelMixin):
    serializer_class = ShoppingListSerializer

    def get_object(self):
        return get_object_or_404(ShoppingList, pk=self.kwargs['pk'])

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

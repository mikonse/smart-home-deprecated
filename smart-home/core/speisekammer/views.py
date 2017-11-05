from rest_framework import permissions
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response

from .models import Product, ShoppingList, Barcode, ShoppingListItem
from .serializers import ProductSerializer, ShoppingListSerializer, BarcodeSerializer, ShoppingListItemSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """
    Viewset for API interaction with the Product model
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    @list_route(methods=['post'], url_path='item-io-by-barcode')
    def item_io_by_barcode(self, request):
        if 'item_io' in request.POST and 'barcode' in request.POST:
            success = Product.item_io_by_barcode(request.POST.get('item_io'), request.POST.get('barcode'))
            if success:
                return Response(
                    self.serializer_class(Barcode.objects.get(request.POST.get('barcode')).product).data,
                    status.HTTP_200_OK
                )
            else:
                return Response(
                    {'error': 'Barcode does not exist in the database or invalid data format.'},
                    status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {'error': 'Invalid request. item_io and barcode keywords must be present in POST data.'},
                status.HTTP_400_BAD_REQUEST
            )

    @detail_route(methods=['post'], url_path='stock-io')
    def stock_io(self, request, pk=None):
        """
        API call to modify the desired stock count of a product.
        POST parameters:
        :stock_count int : io to be performed
        """
        instance = self.get_object()

        if 'stock_io' in request.POST:
            success = instance.stock_io(request.POST.get('stock_io'))
            return Response(
                self.serializer_class(instance, context={'request': request}).data,
                status.HTTP_200_OK if success else status.HTTP_400_BAD_REQUEST
            )
        else:
            return Response(
                {'error': 'Invalid request. item_io keyword must be present in POST data.'},
                status.HTTP_400_BAD_REQUEST
            )

    @detail_route(methods=['post'], url_path='item-io')
    def item_io(self, request, pk=None):
        """
        API call to modify the current item count of a product.
        POST parameters:
        :item_count int : io to be performed
        """
        instance = self.get_object()

        if 'item_io' in request.POST:
            success = instance.item_io(request.POST.get('item_io'))
            return Response(
                self.serializer_class(instance, context={'request': request}).data,
                status.HTTP_200_OK if success else status.HTTP_400_BAD_REQUEST
            )
        else:
            return Response(
                {'error': 'Invalid request. item_io keyword must be present in POST data.'},
                status.HTTP_400_BAD_REQUEST
            )

    @detail_route(methods=['post'], url_path='assign-barcode')
    def assign_barcode(self, request, pk=None):
        instance = self.get_object()

        if 'barcode' in request.POST:
            success = instance.assign_barcode(request.POST.get('barcode'))
            return Response(
                self.serializer_class(instance, context={'request': request}).data,
                status.HTTP_201_CREATED if success else status.HTTP_400_BAD_REQUEST
            )
        else:
            return Response(
                {'error': 'Invalid request. barcode keyword must be present in POST data.'},
                status.HTTP_400_BAD_REQUEST
            )

    @detail_route(methods=['post'], url_path='to-active-list')
    def to_active_list(self, request, pk=None):
        instance = self.get_object()

        if 'amount' in request.POST:
            instance.to_active_list(request.POST.get('amount'))
            return Response(
                self.serializer_class(instance, context={'request': request}).data,
                status.HTTP_201_CREATED
            )
        else:
            return Response(
                {'error': 'Invalid erquest.'},
                status.HTTP_400_BAD_REQUEST
            )


class BarcodeViewSet(viewsets.ModelViewSet):
    """
    Viewset for API interaction with the Barcode model
    """
    queryset = Barcode.objects.all()
    serializer_class = BarcodeSerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class ShoppingListViewSet(viewsets.ModelViewSet):
    """
    Viewset for API interaction with the ShoppingList model
    """
    queryset = ShoppingList.objects.all()
    serializer_class = ShoppingListSerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    @list_route(methods=['post'], url_path='create-from-speisekammer')
    def create_from_speisekammer(self, request):
        """
        API call to automatically generate a shopping list from the current stock.
        """
        name = request.POST.get('name', '')
        instance = ShoppingList.create_from_speisekammer(name=name)

        return Response(
            self.serializer_class(instance, context={'request': request}).data,
            status.HTTP_201_CREATED
        )


class ShoppingListItemViewSet(viewsets.ModelViewSet):
    """
    Viewset for API interaction with the ShoppingListItem model.
    """
    queryset = ShoppingListItem.objects.all()
    serializer_class = ShoppingListItemSerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    @detail_route(methods=['post'], url_path='item-io')
    def item_io(self, request, pk=None):
        """
        API call to modify the current item count of a product.
        POST parameters:
        :item_count int : io to be performed
        """
        instance = self.get_object()

        if 'item_io' in request.POST:
            success = instance.item_io(request.POST.get('item_io'))
            return Response(
                self.serializer_class(instance, context={'request': request}).data,
                status.HTTP_200_OK if success else status.HTTP_400_BAD_REQUEST
            )
        else:
            return Response(
                {'error': 'Invalid request. item_io keyword must be present in POST data.'},
                status.HTTP_400_BAD_REQUEST
            )

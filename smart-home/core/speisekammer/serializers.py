from rest_framework import serializers
from .models import Product, ShoppingList, ShoppingListItem, Barcode


class BarcodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Barcode
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    barcodes = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='api:speisekammer:barcode-detail'
    )

    class Meta:
        model = Product
        fields = '__all__'


class ShoppingListItemSerializer(serializers.ModelSerializer):
    product = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='api:speisekammer:product-detail'
    )

    class Meta:
        model = ShoppingListItem
        fields = '__all__'


class ShoppingListSerializer(serializers.ModelSerializer):
    items = ShoppingListItemSerializer(many=True, read_only=True)

    class Meta:
        model = ShoppingList
        fields = '__all__'

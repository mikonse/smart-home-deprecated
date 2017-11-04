from rest_framework import serializers
from .models import Product, ProductInstance, ShoppingList, ShoppingListItem


class InstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductInstance
        fields = '__all__'


class ItemCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductInstance
        fields = ['item_count']


class ProductSerializer(serializers.ModelSerializer):
    instances = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='api:speisekammer:product_instance_detail'
    )

    class Meta:
        model = Product
        fields = '__all__'


class ShoppingListItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingListItem
        fields = '__all__'


class ShoppingListSerializer(serializers.ModelSerializer):
    items = ShoppingListItemSerializer(many=True, read_only=True)

    class Meta:
        model = ShoppingList
        fields = '__all__'

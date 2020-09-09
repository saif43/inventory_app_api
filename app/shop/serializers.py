from rest_framework import serializers
from core import models


class ShopSerializer(serializers.ModelSerializer):
    """Serializer for shop"""

    # owner = serializers.PrimaryKeyRelatedField(
    #     many=True, queryset=User.objects.filter(is_owner=True)
    # )
    owner = serializers.PrimaryKeyRelatedField(
        queryset=models.User.objects.filter(is_owner=True)
    )

    class Meta:
        model = models.Shop
        fields = ("id", "name", "money", "owner")
        read_only_fields = ("id",)


class WarehouseSerializer(serializers.ModelSerializer):
    """Serializer for warehouse"""

    # if we like to show shop details
    # shop = ShopSerializer(read_only=True)

    class Meta:
        model = models.Warehouse
        fields = ("id", "name", "shop")
        read_only_fields = ("id", "shop")


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for product"""

    class Meta:
        model = models.Product
        fields = ("id", "name", "price", "stock", "shop")
        read_only_fields = ("id", "shop")


class CustomerSerializer(serializers.ModelSerializer):
    """Serializer for Customer"""

    class Meta:
        model = models.Customer
        fields = ("id", "name", "contact", "shop")
        read_only_fields = ("id", "shop")


class VendorSerializer(serializers.ModelSerializer):
    """Serializer for Customer"""

    class Meta:
        model = models.Vendor
        fields = ("id", "name", "contact", "shop")
        read_only_fields = ("id", "shop")

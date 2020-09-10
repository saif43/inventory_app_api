from rest_framework import serializers
from core import models


class ShopSerializer(serializers.ModelSerializer):
    """Serializer for shop"""

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


class CustomerTrasnscationSerializer(serializers.ModelSerializer):
    """Serializer for customer product transaction"""

    def __init__(self, *args, **kwargs):
        """Filter customers by shop"""

        # many = kwargs.pop("many", True)
        super(CustomerTrasnscationSerializer, self).__init__(*args, **kwargs)

        own_shop = models.Shop.objects.get(owner=self.context["request"].user)
        self.fields["customer"].queryset = models.Customer.objects.filter(shop=own_shop)
        self.fields["product"].queryset = models.Product.objects.filter(shop=own_shop)

    class Meta:
        model = models.CustomerTrasnscation
        fields = ("id", "order_time", "shop", "customer", "product", "quantity")
        read_only_fields = ("id", "shop")


class CustomerOrderedItemsSerializer(serializers.ModelSerializer):
    """Serializer for ordered products"""

    # def __init__(self, *args, **kwargs):
    #     """Filter customers by shop"""

    #     # many = kwargs.pop("many", True)
    #     super(CustomerOrderedItemsSerializer, self).__init__(*args, **kwargs)

    #     own_shop = models.Shop.objects.get(owner=self.context["request"].user)
    #     self.fields["order"].queryset = models.CustomerTrasnscation.objects.filter(
    #         shop=own_shop
    #     )

    #     print(len(self.fields["order"].queryset))

    order = serializers.PrimaryKeyRelatedField(
        many=True, queryset=models.CustomerTrasnscation.objects.all()
    )

    class Meta:
        model = models.CustomerOrderedItems
        fields = ("id", "order", "shop")
        read_only_fields = ("id", "shop")

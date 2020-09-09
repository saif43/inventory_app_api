from core.models import Shop, Warehouse, Product, Customer, Vendor
from shop import serializers

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from shop.permissions import (
    ShopAccessPermission,
    WarehouseAccessPermission,
    ProductAccessPermission,
    CustomerAccessPermission,
    VendorAccessPermission,
)


class ShopViewSet(viewsets.ModelViewSet):
    """Manage shops"""

    queryset = Shop.objects.all()
    serializer_class = serializers.ShopSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (ShopAccessPermission,)

    # def get_queryset(self):
    #     if self.request.user.is_superuser:
    #         return self.queryset

    #     return self.queryset.filter(user__id=self.request.user.id)


class BaseShopAttr(viewsets.ModelViewSet):
    """Base class for WarehouseViewSet and ProductViewSet"""

    authentication_classes = (TokenAuthentication,)

    def perform_create(self, serializer):
        own_shop = Shop.objects.get(owner=self.request.user)
        serializer.save(shop=own_shop)

    def get_queryset(self):
        own_shop = Shop.objects.get(owner=self.request.user)
        return self.queryset.filter(shop=own_shop)


class WarehouseViewSet(BaseShopAttr):
    """Manage warehouses"""

    queryset = Warehouse.objects.all()
    serializer_class = serializers.WarehouseSerializer
    permission_classes = (WarehouseAccessPermission,)


class ProductViewSet(BaseShopAttr):
    """Manage products"""

    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer
    permission_classes = (ProductAccessPermission,)


class CustomerViewSet(BaseShopAttr):
    """Manage customer"""

    queryset = Customer.objects.all()
    serializer_class = serializers.CustomerSerializer
    permission_classes = (CustomerAccessPermission,)


class VendorViewSet(BaseShopAttr):
    """Manage vendor"""

    queryset = Vendor.objects.all()
    serializer_class = serializers.VendorSerializer
    permission_classes = (VendorAccessPermission,)

from core.models import (
    Shop,
    Warehouse,
    Product,
    Customer,
    Vendor,
    CustomerTrasnscation,
    CustomerOrderedItems,
)
from shop import serializers

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from shop.permissions import (
    ShopAccessPermission,
    WarehouseAccessPermission,
    ProductAccessPermission,
    CustomerAccessPermission,
    VendorAccessPermission,
    CustomerTransactionPermission,
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


class CustomerTrasnscationViewSet(BaseShopAttr):
    """Manage transaction of customer"""

    queryset = CustomerTrasnscation.objects.all()
    serializer_class = serializers.CustomerTrasnscationSerializer
    permission_classes = (CustomerTransactionPermission,)


class CustomerOrderedItemsViewSet(viewsets.ModelViewSet):
    """Manage customer ordered items of a single order"""

    authentication_classes = (TokenAuthentication,)
    queryset = CustomerOrderedItems.objects.all()
    serializer_class = serializers.CustomerOrderedItemsSerializer
    permission_classes = (CustomerTransactionPermission,)

    def perform_create(self, serializer):
        own_shop = Shop.objects.get(owner=self.request.user)
        serializer.save(shop=own_shop)

    def get_queryset(self):
        own_shop = Shop.objects.get(owner=self.request.user)
        return self.queryset.filter(shop=own_shop)

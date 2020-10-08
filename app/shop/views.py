from core import models
from shop import serializers

from rest_framework import viewsets, status, filters, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view

from rest_framework.authentication import TokenAuthentication
from shop.permissions import (
    ShopAccessPermission,
    WarehouseAccessPermission,
    ProductAccessPermission,
    CustomerAccessPermission,
    VendorAccessPermission,
    CustomerTransactionPermission,
    CustomerOrderedItemsPermission,
    CustomerTrasnscationBillPermission,
    CustomerTrasnscationDueListPermission,
    MoveProductPermission,
)


def getShop(user):
    if user.is_owner:
        return models.Shop.objects.get(owner=user)

    if user.is_manager or user.is_salesman:
        created_by = user.created_by
        return models.Shop.objects.get(owner=created_by)


class ShopViewSet(viewsets.ModelViewSet):
    """Manage shops"""

    queryset = models.Shop.objects.all()
    serializer_class = serializers.ShopSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (ShopAccessPermission,)

    def get_queryset(self):
        if not self.request.user.is_superuser:
            own_shop = getShop(self.request.user)
            return self.queryset.filter(pk=own_shop.id)

        return self.queryset

    def get_serializer_class(self):
        if self.request.user.is_superuser:
            return serializers.AdminShopSerializer

        return serializers.ShopSerializer


class BaseShopAttr(viewsets.ModelViewSet):
    """Base class for WarehouseViewSet and ProductViewSet"""

    authentication_classes = (TokenAuthentication,)

    def perform_create(self, serializer):
        own_shop = getShop(self.request.user)
        print(own_shop)
        serializer.save(shop=own_shop)

    # def get_queryset(self):
    #     own_shop = getShop(self.request.user)
    #     return self.queryset.filter(shop=own_shop)


class WarehouseViewSet(BaseShopAttr):
    """Manage warehouses"""

    queryset = models.Warehouse.objects.all()
    serializer_class = serializers.WarehouseSerializer
    permission_classes = (WarehouseAccessPermission,)


class WarehouseProductsView(BaseShopAttr):
    """Manage products in Warehouse"""

    queryset = models.WareHouseProducts.objects.all()
    serializer_class = serializers.WarehouseProductsSerializer
    permission_classes = (WarehouseAccessPermission,)


class ProductViewSet(BaseShopAttr):
    """Manage products"""

    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    permission_classes = (ProductAccessPermission,)


class SalesmanViewSet(APIView):
    authentication_classes = (TokenAuthentication,)

    def get(self, request, format=None):
        queryset = models.User.objects.all()
        queryset = queryset.filter(
            created_by=getShop(self.request.user).owner, is_salesman=True
        )
        return Response(serializers.SalesmanSerializer(queryset, many=True).data)


class ManagerViewSet(APIView):
    authentication_classes = (TokenAuthentication,)

    def get(self, request, format=None):
        queryset = models.User.objects.all()
        queryset = queryset.filter(
            created_by=getShop(self.request.user).owner, is_manager=True
        )
        return Response(serializers.SalesmanSerializer(queryset, many=True).data)


class CustomerViewSet(BaseShopAttr):
    """Manage customer"""

    queryset = models.Customer.objects.all()
    serializer_class = serializers.CustomerSerializer
    permission_classes = (CustomerAccessPermission,)


class VendorViewSet(BaseShopAttr):
    """Manage vendor"""

    queryset = models.Vendor.objects.all()
    serializer_class = serializers.VendorSerializer
    permission_classes = (VendorAccessPermission,)


class CustomerTrasnscationViewSet(BaseShopAttr):
    """Manage transaction of customer"""

    queryset = models.CustomerTrasnscation.objects.all()
    serializer_class = serializers.CustomerTrasnscationSerializer
    permission_classes = (CustomerTransactionPermission,)


class CustomerOrderedItemsViewSet(viewsets.ModelViewSet):
    """Manage customer ordered items of a single order"""

    authentication_classes = (TokenAuthentication,)
    queryset = models.CustomerOrderedItems.objects.all()
    serializer_class = serializers.CustomerOrderedItemsSerializer
    permission_classes = (CustomerOrderedItemsPermission,)

    filter_backends = (filters.SearchFilter,)
    search_fields = ("=order__id",)
    """
    '^' Starts-with search.
    '=' Exact matches.
    '@' Full-text search. (Currently only supported Django's PostgreSQL backend.)
    '$' Regex search.
    """

    def perform_create(self, serializer):
        own_shop = getShop(self.request.user)
        serializer.save(shop=own_shop)

    def get_queryset(self):
        own_shop = getShop(self.request.user)
        return self.queryset.filter(shop=own_shop)

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return serializers.CustomerOrderedItemsUpdateSerializer

        return self.serializer_class

    # def retrieve(self, request, *args, **kwargs):
    #     """overriding retrieve function, to get result of list of transaction filtered by order_id"""

    #     # do your customization here
    #     # instance = self.get_object()
    #     # # instance = CustomerOrderedItems.objects.filter(order=self.kwargs[])
    #     # print(instance.id)
    #     try:
    #         # http://api/kwargs['pk']
    #         transaction = CustomerTrasnscation.objects.filter(pk=kwargs['pk'])

    #         instance = CustomerOrderedItems.objects.filter(
    #             order=transaction[0])

    #         serialized_data = []

    #         for i in instance:
    #             serialize = self.get_serializer(i)
    #             serialized_data.append(serialize.data)

    #         return Response(serialized_data, status=status.HTTP_200_OK)

    #     except:
    #         return Response(status=status.HTTP_404_NOT_FOUND)


class CustomerTrasnscationBillViewSet(BaseShopAttr):
    """Manage bill of a transaction"""

    queryset = models.CustomerTrasnscationBill.objects.all()
    serializer_class = serializers.CustomerTrasnscationBillSerializer
    permission_classes = (CustomerTrasnscationBillPermission,)

    filter_backends = (filters.SearchFilter,)
    search_fields = ("=order__id",)
    """
    '^' Starts-with search.
    '=' Exact matches.
    '@' Full-text search. (Currently only supported Django's PostgreSQL backend.)
    '$' Regex search.
    """


class CustomerDueListViewSet(BaseShopAttr):
    """Show customer transactions who has due"""

    serializer_class = serializers.CustomerTrasnscationBillSerializer
    permission_classes = (CustomerTrasnscationDueListPermission,)

    def get_queryset(self):
        own_shop = getShop(self.request.user)
        return models.CustomerTrasnscationBill.objects.filter(shop=own_shop, due__gt=0)


class VendorTrasnscationViewSet(BaseShopAttr):
    """Manage transaction of Vendor"""

    queryset = models.VendorTrasnscation.objects.all()
    serializer_class = serializers.VendorTrasnscationSerializer
    permission_classes = (CustomerTransactionPermission,)


class VendorOrderedItemsViewSet(viewsets.ModelViewSet):
    """Manage Vendor ordered items of a single order"""

    authentication_classes = (TokenAuthentication,)
    queryset = models.VendorOrderedItems.objects.all()
    serializer_class = serializers.VendorOrderedItemsSerializer
    permission_classes = (CustomerOrderedItemsPermission,)

    filter_backends = (filters.SearchFilter,)
    search_fields = ("=order__id",)

    def perform_create(self, serializer):
        own_shop = getShop(self.request.user)
        serializer.save(shop=own_shop)

    def get_queryset(self):
        own_shop = getShop(self.request.user)
        return self.queryset.filter(shop=own_shop)


class VendorTrasnscationBillViewSet(BaseShopAttr):
    """Manage bill of a transaction"""

    queryset = models.VendorTrasnscationBill.objects.all()
    serializer_class = serializers.VendorTrasnscationBillSerializer
    permission_classes = (CustomerTrasnscationBillPermission,)


class MoveProductViewSet(BaseShopAttr):
    """Moving products shop to warehouse"""

    queryset = models.MoveProduct.objects.all()
    serializer_class = serializers.MoveProductSerializer
    permission_classes = (MoveProductPermission,)

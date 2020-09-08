from core.models import Shop
from shop import serializers

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from shop.permissions import AccessPermission


class ShowViewSet(viewsets.ModelViewSet):
    """Manage shops"""

    queryset = Shop.objects.all()
    serializer_class = serializers.ShopSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AccessPermission,)
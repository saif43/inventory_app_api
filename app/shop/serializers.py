from rest_framework import serializers
from core.models import Shop

class ShopSerializer(serializers.ModelSerializer):
    """Serializer for shop"""

    class Meta:
        model = Shop
        fields = ('id', 'name')
        read_only_fields = ('id')


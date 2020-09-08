from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User object"""

    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "name",
            "password",
        )

        extra_kwargs = {
            "password": {
                "write_only": True,
                "min_length": 5,
                "style": {"input_type": "password"},
            }
        }
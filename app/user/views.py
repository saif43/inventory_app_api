from rest_framework import generics, authentication, permissions, mixins
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework import status, viewsets, filters

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication


from user.permissions import ProfileAccessPermission
from user import serializers
from core import models


class CreateUserAPIView(generics.CreateAPIView):
    """Creates a new user in the system"""

    serializer_class = serializers.UserSerializer


class UserListView(viewsets.ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (ProfileAccessPermission,)


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""

    serializer_class = serializers.AuthtokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""

    serializer_class = serializers.UserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        """Retrive and return authenticated user"""
        return self.request.user

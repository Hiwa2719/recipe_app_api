from django.contrib.auth import get_user_model
from rest_framework import generics, authentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import TokenAuthentication
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated

from .serializers import UserSerializer, AuthTokenSerializer

User = get_user_model()


class CreateUserView(generics.CreateAPIView):
    """handles creating new users"""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create new auth token for view"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """this class handle me_url and managing user info"""
    serializer_class = UserSerializer
    authentication_classes = authentication.TokenAuthentication,
    permission_classes = IsAuthenticated,

    def get_object(self):
        return self.request.user

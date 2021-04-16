from django.shortcuts import render
from rest_framework import generics, permissions, authentication

from .serializers import TagSerializer
from core.models import Tag


class TagsList(generics.ListAPIView):
    serializer_class = TagSerializer
    authentication_classes = authentication.TokenAuthentication,
    permission_classes = permissions.IsAuthenticated,

    def get_queryset(self):
        return Tag.objects.filter(creator=self.request.user)

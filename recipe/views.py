from rest_framework import permissions, authentication, viewsets, mixins

from .serializers import TagSerializer
from core.models import Tag


class TagsList(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = TagSerializer
    authentication_classes = authentication.TokenAuthentication,
    permission_classes = permissions.IsAuthenticated,

    def get_queryset(self):
        return Tag.objects.filter(creator=self.request.user)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

from rest_framework import permissions, authentication, viewsets, mixins

from .serializers import TagSerializer, IngredientSerializer
from core.models import Tag, Ingredient


class TagsViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = TagSerializer
    authentication_classes = authentication.TokenAuthentication,
    permission_classes = permissions.IsAuthenticated,

    def get_queryset(self):
        return Tag.objects.filter(creator=self.request.user)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class IngredientsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = IngredientSerializer
    permission_classes = permissions.IsAuthenticated,
    authentication_classes = authentication.TokenAuthentication,

    def get_queryset(self):
        return Ingredient.objects.filter(creator=self.request.user)

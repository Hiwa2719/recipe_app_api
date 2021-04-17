from rest_framework import permissions, authentication, viewsets, mixins

from .serializers import TagSerializer, IngredientSerializer
from core.models import Tag, Ingredient


class BaseRecipeAttrViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    """Base view for recipe attributes"""
    # serializer_class =
    authentication_classes = authentication.TokenAuthentication,
    permission_classes = permissions.IsAuthenticated,

    def get_queryset(self):
        """only objects created by user should be returned"""
        return self.queryset.filter(creator=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class TagsViewSet(BaseRecipeAttrViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class IngredientsViewSet(BaseRecipeAttrViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()

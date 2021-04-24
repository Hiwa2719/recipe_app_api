from rest_framework import permissions, authentication, viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.views import View
from .serializers import (TagSerializer, IngredientSerializer, RecipeSerializer, RecipeDetailSerializer,
                          RecipeImageSerializer)
from core.models import Tag, Ingredient, Recipe


class BaseRecipeAttrViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    """Base view for recipe attributes"""
    authentication_classes = authentication.TokenAuthentication,
    permission_classes = permissions.IsAuthenticated,

    def get_queryset(self):
        """only objects created by user should be returned"""
        assigned_only = int(self.request.query_params.get('assigned_only', 0))
        queryset = super().get_queryset()
        if assigned_only:
            queryset = queryset.filter(recipe__isnull=False).distinct()
        return queryset.filter(creator=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class TagsViewSet(BaseRecipeAttrViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class IngredientsViewSet(BaseRecipeAttrViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()


class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeSerializer
    permission_classes = permissions.IsAuthenticated,
    authentication_classes = authentication.TokenAuthentication,
    queryset = Recipe.objects.all()

    def _comma_delimited_to_list(self, string):
        """converts comma delimited string to list of integers"""
        return [int(str_id) for str_id in string.split(',')]

    def get_queryset(self):
        tags = self.request.query_params.get('tags')
        ingredients = self.request.query_params.get('ingredients')
        queryset = super().get_queryset()
        if tags:
            tag_ids = self._comma_delimited_to_list(tags)
            queryset = queryset.filter(tags__id__in=tag_ids)
        if ingredients:
            ingredient_ids = self._comma_delimited_to_list(ingredients)
            queryset = queryset.filter(ingredients__id__in=ingredient_ids)
        return queryset.filter(creator=self.request.user)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def get_serializer_class(self):
        """return appropriate serializer"""
        if self.action == 'retrieve':
            return RecipeDetailSerializer
        elif self.action == 'upload_image':
            return RecipeImageSerializer
        return self.serializer_class

    @action(['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """upload an image to a recipe"""
        recipe = self.get_object()
        serializer = self.get_serializer(
            recipe,
            data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

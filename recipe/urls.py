from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'recipe'

router = DefaultRouter()
router.register('tag', views.TagsViewSet, basename='tags')
router.register('ingredient', views.IngredientsViewSet, basename='ingredients')
router.register('recipe', views.RecipeViewSet, basename='recipes')

urlpatterns = [
    path('', include(router.urls)),
]

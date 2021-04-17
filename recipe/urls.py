from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'recipe'

router = DefaultRouter()
router.register('tags-list', views.TagsViewSet, basename='tags')
router.register('ingredient-list', views.IngredientsViewSet, basename='ingredients')


urlpatterns = [
    path('', include(router.urls)),
]

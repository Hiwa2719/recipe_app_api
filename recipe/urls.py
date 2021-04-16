from django.urls import path

from . import views

app_name = 'recipe'


urlpatterns = [
    path('tags-list/', views.TagsList.as_view(), name='tags-list'),
]

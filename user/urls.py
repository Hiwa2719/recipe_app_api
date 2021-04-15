from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('user', views.UserViewSet)
app_name = 'user'


urlpatterns = [
    path('', include(router.urls)),
    path('token/', views.CreateTokenView.as_view(), name='token'),
]

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from core.models import Ingredient
from recipe.serializers import IngredientSerializer

User = get_user_model()
ingredient_url = reverse('recipe:ingredients-list')


class PublicIngredientApiTests(APITestCase):
    """Writing ingredients tests here"""
    def test_login_required(self):
        """testing login required for accessing this endpoint"""
        response = self.client.get(ingredient_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientApiTests(APITestCase):
    """testing Ingredient Api while user is authenticated"""
    def setUp(self) -> None:
        self.user = User.objects.create_user(email='hiwa@gmail.com', password='hiwa_asdf')
        self.user2 = User.objects.create_user(email='asdf@gmail.com', password='helloThere')
        Ingredient.objects.create(name='salt', creator=self.user2)
        Ingredient.objects.create(name='pepper', creator=self.user)
        self.client.force_authenticate(self.user2)

    def test_Ingredient_list(self):
        """here we test ingredient-list endpoint"""
        response = self.client.get(ingredient_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ingredients = Ingredient.objects.filter(creator=self.user2)
        serializer = IngredientSerializer(ingredients, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(ingredients.count(), 1)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'salt')

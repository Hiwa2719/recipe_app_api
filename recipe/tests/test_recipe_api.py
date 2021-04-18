from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from core.models import Recipe
from recipe.serializers import RecipeSerializer

User = get_user_model()
RECIPE_URL = reverse('recipe:recipes-list')


def sample_recipe(creator, **kwargs):
    """create and return a sample recipe"""
    default = {
        'title': 'sample recipe',
        'time_minutes': 10,
        'price': 5.00
    }
    default.update(kwargs)
    return Recipe.objects.create(creator=creator, **default)


class PublicRecipeApiTests(APITestCase):
    """testing Recipe api here for anonymouse users"""
    def test_login_required(self):
        """testing that login is required"""
        response = self.client.get(RECIPE_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTest(APITestCase):
    """testing recipe api while user is authenticated"""
    def setUp(self) -> None:
        self.user = User.objects.create_user(email='hiwa@gmail.com', password='hiwa_asdf')
        self.user2 = User.objects.create_user(email='asdf@asdf.com', password='hiwa_asdf')
        self.client.force_authenticate(self.user)

    def test_accessing_recipe_list(self):
        """test accessing recipe list of client"""
        sample_recipe(self.user)
        sample_recipe(self.user2)
        sample_recipe(self.user, title='hello world')
        response = self.client.get(RECIPE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        recipes = Recipe.objects.filter(creator=self.user)
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(len(response.data), 2)

hello world
asdf
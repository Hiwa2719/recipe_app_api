from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from core.models import Ingredient, Recipe
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
        self.ingredient1 = Ingredient.objects.create(name='salt', creator=self.user2)
        self.ingredient2 = Ingredient.objects.create(name='pepper', creator=self.user)
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

    def test_creating_ingredient(self):
        """testing creating ingredients"""
        response = self.client.post(ingredient_url, {'name': 'vinegar'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        ingredient = Ingredient.objects.get(name='vinegar')
        self.assertEqual(ingredient.creator, self.user2)

    def test_filtering_ingredients_assigned_to_recipes(self):
        """retrieving ingredients that are only assigned to recipes"""
        ingredient1 = Ingredient.objects.create(creator=self.user2, name='saltti')
        ingredient2 = Ingredient.objects.create(creator=self.user2, name='ingredient2')
        recipe = Recipe.objects.create(
            creator=self.user2,
            title='hello recipe',
            time_minutes=5,
            price=10.00
        )
        recipe.ingredients.add(ingredient1)

        response = self.client.get(
            ingredient_url,
            data={'assigned_only': 1}
        )
        serializer1 = IngredientSerializer(ingredient1)
        serializer2 = IngredientSerializer(ingredient2)
        self.assertIn(serializer1.data, response.data)
        self.assertNotIn(serializer2.data, response.data)

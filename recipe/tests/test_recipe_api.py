from decimal import Decimal
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from core.models import Recipe, Tag, Ingredient
from recipe.serializers import RecipeSerializer, RecipeDetailSerializer

User = get_user_model()
RECIPE_URL = reverse('recipe:recipes-list')


def sample_tag(creator, name='Crap tag'):
    """Creates a sample tag here"""
    return Tag.objects.create(name=name, creator=creator)


def sample_ingredient(creator, name='crap ingredient'):
    """creates a sample ingredient"""
    return Ingredient.objects.create(name=name, creator=creator)


def sample_recipe(creator, **kwargs):
    """create and return a sample recipe"""
    default = {
        'title': 'sample recipe',
        'time_minutes': 10,
        'price': 5.00
    }
    default.update(kwargs)
    return Recipe.objects.create(creator=creator, **default)


def recipe_detail_url(pk):
    """return recipe detail url"""
    return reverse('recipe:recipes-detail', args=[pk])


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

    def test_recipe_detail_view(self):
        """testing accessing recipe detail view"""
        recipe = sample_recipe(self.user)
        recipe.tags.add(sample_tag(self.user2))
        recipe.ingredients.add(sample_ingredient(self.user))
        response = self.client.get(recipe_detail_url(recipe.id))
        self.assertEqual(response.status_code, 200)
        serializer = RecipeDetailSerializer(recipe)
        self.assertEqual(response.data, serializer.data)

    def test_create_basic_recipe(self):
        """test creating a recipe"""
        data = {
            'title': 'chocolate cheesecake',
            'time_minutes': 30,
            'price': 5.00
        }
        response = self.client.post(RECIPE_URL, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=response.data['id'])
        for key in data.keys():
            self.assertEqual(data[key], getattr(recipe, key))
        self.assertEqual(recipe.creator, self.user)

    def test_creating_recipe_with_tags(self):
        """using tags in recipe creation"""
        tag1 = sample_tag(self.user)
        tag2 = sample_tag(self.user2, name='tagssss')
        data = {
            'title': 'this is a test recipe',
            'time_minutes': 10,
            'price': 10.00,
            'tags': [tag1.id, tag2.id]
        }
        response = self.client.post(RECIPE_URL, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=response.data['id'])
        self.assertIn(tag1, recipe.tags.all())
        self.assertIn(tag2, recipe.tags.all())

    def test_creating_recipe_with_tags_and_ingredients(self):
        """adding tags and ingredients to recipe"""
        tag1 = sample_tag(self.user)
        tag2 = sample_tag(self.user2, name='tagsss')
        ingredient1 = sample_ingredient(self.user2)
        data = {
            'title': 'Coding is fun',
            'time_minutes': 10,
            'price': 50.00,
            'tags': [tag1.id, tag2.id],
            'ingredients': [ingredient1.id]
        }
        response = self.client.post(RECIPE_URL, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=response.data['id'])
        self.assertIn(ingredient1, recipe.ingredients.all())

    def test_partial_update_recipe(self):
        """test recipe partial update"""
        recipe = sample_recipe(self.user)
        recipe.tags.add(sample_tag(self.user, name='curry'))
        new_tag = sample_tag(self.user2, 'hurry')
        data = {
            'title': 'updating recipe',
            'price': 10.00,
            'tags': [new_tag.id]
        }
        response = self.client.patch(recipe_detail_url(recipe.id), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        recipe.refresh_from_db()
        self.assertEqual(data['title'], recipe.title)
        tags = recipe.tags.all()
        self.assertEqual(tags.count(), 1)
        self.assertIn(new_tag, tags)

    def test_update_recipe(self):
        """test update recipe"""
        recipe = sample_recipe(self.user)
        recipe.tags.add(sample_tag(self.user, name='curry'))
        data = {
            'title': 'updating 101',
            'time_minutes': 10,
            'price': 10.00,
        }
        response = self.client.put(recipe_detail_url(recipe.id), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        recipe.refresh_from_db()
        for key in data.keys():
            self.assertEqual(data[key], getattr(recipe, key))
        tags = recipe.tags.all()
        self.assertEqual(tags.count(), 0)


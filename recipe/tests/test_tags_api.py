from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from core.models import Tag, Recipe
from recipe.serializers import TagSerializer

User =get_user_model()
tag_url = reverse('recipe:tags-list')


class TestTagApiAnonymousUser(APITestCase):
    def test_tags_list_authentication(self):
        """testing authentication requirement for tags-list api"""
        response = self.client.get(tag_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestTagApiAuthenticatedUser(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(email='hiwa@gmail.com', password='hiwa_adsf')
        self.user2 = User.objects.create_user(email='asdf@asdf.com', password='hiwa_asdf')
        self.tag1 =Tag.objects.create(name='pizza', creator=self.user)
        self.tag2 = Tag.objects.create(name='sandwich', creator=self.user2)
        self.client.force_authenticate(self.user)

    def test_tags_list_items(self):
        """testing for authenticated user it must return all tags created by him/her"""
        response = self.client.get(tag_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        tags = Tag.objects.filter(creator=self.user)
        serializer = TagSerializer(tags, many=True)
        self.assertEqual(response.data, serializer.data)
        tag = Tag.objects.get(id=response.data[0]['id'])
        self.assertEqual(tag.creator, self.user)

    def test_creating_new_tag(self):
        """tag creation test"""
        response = self.client.post(tag_url, {'name': 'kalana'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        tag = Tag.objects.get(id=response.data.get('id'))
        self.assertEqual(tag.creator, self.user)
        self.assertEqual(response.data.get('name'), 'kalana')

        tag_exists = Tag.objects.filter(name='kalana', creator=self.user).exists()
        self.assertTrue(tag_exists)

    def test_creating_tag_without_name(self):
        """passing blank name to tag creation"""
        response = self.client.post(tag_url, {'name': ''})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        tag_exits = Tag.objects.filter(name='', creator=self.user)
        self.assertFalse(tag_exits)

    def test_retrieve_tags_assigned_to_recipes(self):
        """test filtering tags by those assigned to recipes"""
        tag1 = Tag.objects.create(creator=self.user, name='some tag')
        tag2 = Tag.objects.create(creator=self.user, name='added tag')

        recipe = Recipe.objects.create(
            creator=self.user,
            title='hello world',
            time_minutes=5,
            price=10.00,
        )
        recipe.tags.add(tag1)

        response = self.client.get(
            tag_url,
            data={'assigned_only': 1}
        )

        serializer = TagSerializer(tag1)
        serializer2 = TagSerializer(tag2)
        self.assertIn(serializer.data, response.data)
        self.assertNotIn(serializer2.data, response.data)

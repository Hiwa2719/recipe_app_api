from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from core.models import Tag
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
        Tag.objects.create(name='pizza', creator=self.user)
        Tag.objects.create(name='sandwich', creator=self.user2)
        self.client.force_authenticate(self.user)

    def test_tags_list_items(self):
        """testing for authenticated user it must return all tags created by him/her"""
        response = self.client.get(tag_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        tags = Tag.objects.filter(creator=self.user)
        serializer = TagSerializer(tags, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.data[0]['creator'], self.user.id)
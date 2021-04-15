from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class AnonymousUserApiTests(APITestCase):

    def setUp(self) -> None:
        self.create_url = reverse('user:user-list')
        self.token_url = reverse('user:token')

    def test_create_user(self):
        """test creating user with valid data"""
        data = {
            'email': 'hiwa@gmail.com',
            'password': 'hiwa_asdf',
            'name': 'what ever'
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('hiwa@gmail.com', str(response.content, encoding='utf-8'))
        user = User.objects.get(**response.data)
        self.assertTrue(user.check_password(data['password']))
        self.assertNotIn('password', response.data)

    def test_creating_repetitive_user(self):
        data = {
            'email': 'hiwa@gmail.com',
            'password': 'asdf'
        }
        user = User.objects.create_user(**data).set_password
        response = self.client.post(self.create_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_for_short_password(self):
        data = {
            'email': 'hiwa@gmail.com',
            'password': 'as'
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, 400)
        user_exists = User.objects.filter(email=data['email']).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """test that a token is created for the user"""
        data = {
            'email': 'hiwa@gmail.com',
            'password': 'hiwa_asdf'
        }
        user = User.objects.create_user(**data)
        response = self.client.post(self.token_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_create_token_invalid_credintials(self):
        """tests if we send in invalid credintials"""
        User.objects.create_user(email='hiwa@gmail.com', password='hiwa_asdf')
        data = {
            'email': 'hiwa@gmail.com',
            'password': 'testing 101'
        }
        response = self.client.post(self.token_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', response.data)

    def test_create_token_without_user(self):
        """tests creating token while the user doesn't exists"""
        data = {
            'email': 'hiwa@gmail.com',
            'password': 'hiwa_asdf'
        }

        response = self.client.post(self.token_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', response.data)

    def test_create_token_without_fields(self):
        """test creating token without providing email and pass"""
        response = self.client.post(self.token_url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', response.data)


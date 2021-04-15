from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class ModelTests(TestCase):
    """testing User model"""

    def test_user_creation_with_email(self):
        user = User.objects.create_user(email='hiwa@gmail.com', password="HiWa0426513")

        user = User.objects.get(email='hiwa@gmail.com')
        self.assertEqual(user.email, 'hiwa@gmail.com')
        self.assertTrue(user.check_password('HiWa0426513'))

    def test_new_user_without_email_password(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(password='helloJohn123')

        with self.assertRaises(ValueError):
            User.objects.create_user(email='hwllo@gmail.com')

    def test_create_super_user(self):
        """Creating a new superuser"""
        user = User.objects.create_superuser(email='hello@john.com', password='hello@john.com')

        self.assertEqual(user.email, 'hello@john.com')
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)


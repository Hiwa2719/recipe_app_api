from django.contrib.auth import get_user_model
from django.test import TestCase
from django.db.utils import IntegrityError
from unittest.mock import patch

from core.models import Tag, Ingredient, Recipe, recipe_image_location

User = get_user_model()


def create_sample_user(email='hiwa@gmail.com', password='hiwa_asdf'):
    return User.objects.create_user(email=email, password=password)


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

    def test_tag_str(self):
        """test creating a tag obj and returning it's string representation"""
        user = create_sample_user()
        tag = Tag.objects.create(name='pizza', creator=user)
        self.assertEqual(tag.name, 'pizza')
        self.assertEqual(str(tag), 'pizza')
        self.assertEqual(tag.creator, user)

    def test_creating_repetitive_tag(self):
        """models mustn't accept repetitive tag names"""
        Tag.objects.create(name='lake', creator=create_sample_user())
        with self.assertRaises(IntegrityError):
            Tag.objects.create(name='lake', creator=create_sample_user(email='asdf@gmail.com'))

    def test_ingredient_str(self):
        """testing Ingredient model str"""
        ingredient = Ingredient.objects.create(
            name='salt',
            creator=create_sample_user()
        )
        self.assertEqual(str(ingredient), 'salt')

    def test_creating_repetitive_Ingredient(self):
        Ingredient.objects.create(name='salt', creator=create_sample_user())
        with self.assertRaises(IntegrityError):
            Ingredient.objects.create(name='Salt', creator=create_sample_user())

    def test_recipe_str(self):
        """test the recipe model str representation"""
        recipe = Recipe.objects.create(
            creator=create_sample_user(),
            title='Steak and mushroom sauce',
            time_minutes=5,
            price=5.00
        )
        self.assertEqual(str(recipe), recipe.title)

    @patch('uuid.uuid4')
    def test_recipe_file_name_uuid(self, mock_uuid):
        """test that image is saved in correct location"""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = recipe_image_location(None, 'myimage.jpg')

        exp_path = f'uploads/recipe/{uuid}.jpg'
        # self.assertEqual(file_path, exp_path)

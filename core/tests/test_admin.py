from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class AdminSiteTests(TestCase):

    def setUp(self) -> None:
        self.admin_user = User.objects.create_superuser(email='hiwa@gmail.comm', password='asdf')
        self.client.force_login(self.admin_user)
        self.user = User.objects.create_user(email='hello@gmail.com', password='asdf', name='test for admin')

    def test_users_on_changelist(self):
        """test whether users exist on changelist page"""
        url = reverse('admin:core_user_changelist')
        response = self.client.get(url)
        self.assertContains(response, self.user.email)
        self.assertContains(response, self.admin_user.email)

    def test_user_change_page(self):
        url = reverse('admin:core_user_change', args=[self.user.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.email)
        self.assertContains(response, 'test for admin')

    def test_create_new_user(self):
        url = reverse('admin:core_user_add')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'email')

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class LoginRequiredPasswordChangeTests(TestCase):
    def test_reduction(self):
        url = reverse('password_change')
        login_url = reverse('login')
        response = self.client.get(url)
        self.assertRedirects(response, f'{login_url}?next={url}')


class PasswordChangeTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testuser@test.com', password='old_password')
        self.url = reverse('password_change')
        self.client.login(username='testuser', password='old_password')
        self.response = self.client.post(self.url, data)
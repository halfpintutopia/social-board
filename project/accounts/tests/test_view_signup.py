# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse

from accounts.views import signup
from accounts.forms import SignUpForm


class SignUpTests(TestCase):
    def setUp(self):
        url = reverse('signup')
        self.response = self.client.get(url)

    def test_signup_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_signup_url_resolves_signup_view(self):
        view = resolve('/signup/')
        self.assertEquals(view.func, signup)

    def csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, SignUpForm)

    def test_form_inputs(self):
        """
        Case: if a new developer wanted to re-use the SignUpForm for something else,
        then those new fields would also show up in the signup.html or the change could pass unnoticed.
        Test: verifies the HTML inputs in the template.
        The view must contain five inputs: csrf, username, email, password1, password2
        """
        self.assertContains(self.response, '<input', 5)
        self.assertContains(self.response, 'type="text"', 1)
        self.assertContains(self.response, 'type="email"', 1)
        self.assertContains(self.response, 'type="password"', 2)


class SuccessfulSignUpTests(TestCase):
    def setUp(self):
        url = reverse('signup')
        data = {
            'username': 'testuser123',
            'email': 'test@test.com',
            'password1': 'qwertz123',
            'password2': 'qwertz123'
        }
        self.response = self.client.post(url, data)
        self.home_url = reverse('home')

    def test_redirection(self):
        """A valid form submission should redirect the user to the home page."""
        self.assertRedirects(self.response, self.home_url)

    def test_user_creation(self):
        self.assertTrue(User.objects.exists())

    def test_user_authenticate(self):
        """
        Create a new request to an arbitary page.
        The resulting response should now have 'user' to its context,
        after a successful sign up.
        """
        response = self.client.get(self.home_url)
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)


class InvalidSignUpTests(TestCase):
    def setUp(self):
        url = reverse('signup')
        self.response = self.client.post(url, {})  # submit an empty dictionary.

    def test_signup_status_code(self):
        """An invalid form submission should return to the same page."""
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_dont_create_user(self):
        self.assertFalse(User.objects.exists())

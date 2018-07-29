from django.test import TestCase
from ..forms import SignUpForm


class SignUpFormTest(TestCase):
    def test_form_has_fields(self):
        """Test to alert us if code changes in the future and requires tweaks."""
        form = SignUpForm()
        expected = ['username', 'email', 'password1', 'password2']
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)

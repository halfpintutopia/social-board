from django.urls import reverse, resolve
# from django.core.urlresolvers import reverse # module was moved to django.urls
from django.test import TestCase

from boards.views import home


class HomeTests(TestCase):
    """Test the status code of the response."""

    def test_home_view_status_code(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    """Test correct view function for requested URL."""

    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func, home)

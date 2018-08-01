from django.test import TestCase
from django.urls import reverse, resolve

from boards.models import Board
from boards.views import home


class HomeTests(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name='Django', description='Django board.')
        url = reverse('home')
        self.response = self.client.get(url)

    def test_home_view_status_code(self):
        """Test the status code of the response."""
        # url = reverse('home')
        # response = self.client.get(url)
        self.assertEquals(self.response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        """Test correct view function for requested URL."""
        view = resolve('/')
        self.assertEquals(view.func, home)

    def test_home_view_contains_link_to_topics_page(self):
        board_topics_url = reverse('board_topics', kwargs={'pk': self.board.pk})
        self.assertContains(self.response, 'href="{0}"'.format(board_topics_url))

    # def test_board_topics_view_contains_link_back_to_homepage(self):
    #     board_topics_url = reverse('board_topics', kwargs={'pk': 1})
    #     response = self.client.get(board_topics_url)
    #     homepage_url = reverse('home')
    #     self.assertContains(response, 'href="{0}"'.format(homepage_url))

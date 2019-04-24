from django.test import TestCase
from django.urls import reverse, resolve
from posts import views


class TestUrls(TestCase):

    def test_view_create_new_post_url_is_resolved(self):
        url = reverse('posts:newPost')
        self.assertEqual(resolve(url).func, views.create_new_post)
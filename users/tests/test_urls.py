from django.test import SimpleTestCase
from django.urls import reverse, resolve
from users.views import *


class TestUrls(SimpleTestCase):

    def test_test_url_is_resolved(self):
        assert 1 == 1

    def test_view_profile_url_is_resolved(self):
        url = reverse('users:view_profile')
        self.assertEqual(resolve(url).func, view_profile)
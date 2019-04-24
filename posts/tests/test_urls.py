from django.test import TestCase
from django.urls import reverse, resolve
from posts import views
from users.models import Course


class TestUrls(TestCase):

    def setUp(self):
        self.course = Course.objects.create(
            course_id=1,
            course_name='OOP'
        )

    def test_view_create_new_post_url_is_resolved(self):
        url = reverse('posts:newPost')
        self.assertEqual(resolve(url).func, views.create_new_post)

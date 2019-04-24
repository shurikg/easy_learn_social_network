from django.test import TestCase
from django.urls import reverse, resolve
from posts import views
from users.models import Course


class TestUrls(TestCase):

    def setUp(self):
        self.oop_course = Course(1, 'OOP')
        self.oop_course.save()

    def test_view_create_new_post_url_is_resolved(self):
        url = reverse('posts:newPost')
        self.assertEqual(resolve(url).func, views.create_new_post)

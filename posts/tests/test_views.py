from django.contrib.auth.models import User
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse

from posts.models import Post


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

        # create user
        self.username = 'testuser'
        self.email = 'test@test.com'
        self.password = '12345'
        self.user = User(username=self.username, email=self.email)
        self.user.set_password(self.password)
        self.user.save()
        login = self.client.login(username=self.username, password=self.password)
        self.assertEqual(login, True)

    def test_test_view(self):
        assert 1 == 1

    def test_publish_private_post(self):
        new_post = Post(category='other', body='unit test post', author=self.user)
        new_post.save()
        pk = new_post.id
        response = self.client.post(reverse('posts:post-detail', args=(pk,)))
        self.assertEqual(response.status_code, 200)

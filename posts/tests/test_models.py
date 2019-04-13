from django.test import TestCase
from posts.models import Post, Comments
from django.contrib.auth.models import User


class TestModels(TestCase):

    def setUp(self):

        # create user
        self.username = 'testuser'
        self.email = 'test@test.com'
        self.password = '12345'
        self.user = User(username=self.username, email=self.email)
        self.user.set_password(self.password)
        self.user.save()
        login = self.client.login(username=self.username, password=self.password)
        self.assertEqual(login, True)

        # create post
        self.post1 = Post.objects.create(
            category='Other',
            body='test1',
            author=self.user
        )

    def test_post_is_assigned_slug_on_creation(self):
        self.assertEqual(self.post1.category, 'Other')
        self.assertEqual(self.post1.body, 'test1')

    def test_post_not_exits(self):
        self.assertNotEqual(self.post1.category, 'Other1')
        self.assertNotEqual(self.post1.body, 'test11')


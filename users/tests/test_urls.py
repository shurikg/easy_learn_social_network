from django.test import TestCase
from django.urls import reverse, resolve
from users.views import *


class TestUrls(TestCase):

    def setUp(self):
        # create user
        username = 'testuser'
        email = 'test@test.com'
        password = '12345'
        self.user = User(username=username, email=email)
        self.user.set_password(password)
        self.user.save()
        login = self.client.login(username=username, password=password)
        self.assertEqual(login, True)

    def test_test_url_is_resolved(self):
        assert 1 == 1

    def test_view_profile_url_is_resolved(self):
        url = reverse('users:view_profile')
        self.assertEqual(resolve(url).func, view_profile)

    def test_edit_profile_url_is_resolved(self):
        url = reverse('users:edit_profile')
        self.assertEqual(resolve(url).func, edit_profile)

    def test_list_of_friends_url_is_is_resolved(self):
        user_id = self.user.id
        url = reverse('users:list_of_friends', args=(user_id,))
        self.assertEqual(resolve(url).func, list_of_friends)

    def test_show_selected_user_url_is_is_resolved(self):
        user_id = self.user.id
        url = reverse('users:selected_user', args=(user_id,))
        self.assertEqual(resolve(url).func, show_selected_user)

    def test_accept_friend_request_is_resolved(self):
        user_id = self.user.id
        url = reverse('users:accept_friend_request', args=(user_id,))
        self.assertEqual(resolve(url).func, accept_friend_request)


from django.test import TestCase
from django.contrib.auth.models import User
from users.models import Profile,FriendRequest


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

        # create profile
        self.profile = Profile.objects.create(
            user=self.user,
            birth_date='1999-1-1',
            gender='male',
            college_name='SCE',
            year_of_study='3',
            about_me='some text'
        )

        self.friend_request = FriendRequest.objects.create(
            from_user=self.user,
            to_user=self.user
        )

    def test_some_test(self):
        assert 1 == 1

    # test creation profile
    def test_profile_is_assigned_slug_on_creation(self):
        self.assertEqual(self.profile.birth_date, '1999-1-1')
        self.assertEqual(self.profile.gender, 'male')
        self.assertEqual(self.profile.college_name, 'SCE')
        self.assertEqual(self.profile.year_of_study, '3')
        self.assertEqual(self.profile.about_me, 'some text')

    def test_to_user_friend_request_slug_on_creation(self):
        self.assertEqual(self.friend_request.to_user, self.user)

    def test_from_user_friend_request_slug_on_creation(self):
        self.assertEqual(self.friend_request.from_user, self.user)

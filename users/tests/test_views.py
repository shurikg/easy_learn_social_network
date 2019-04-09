from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from users.models import Profile, Privacy, Course, Degree, UserCourses, UserDegrees


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()

        self.view_profile_url = reverse('users:view_profile')
        self.edit_profile_url = reverse('users:edit_profile')
        self.edit_privacy_url = reverse('users:edit_privacy')

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

        # create privacy
        self.privacy = Privacy.objects.create(
            user=self.user,
            privacy_birth_date=False,
            privacy_gender=False,
            privacy_college_name=True,
            privacy_year_of_study=False,
            privacy_about_me=True
        )

        self.course = Course.objects.create(
            course_id='1',
            course_name='text_course'
        )
        self.degree = Degree.objects.create(
            degree_id='1',
            degree_name='text_degree'
        )
        self.userCourses = UserCourses.objects.create(
            user_id=self.profile,
            course_id=self.course
        )
        self.userDegrees = UserDegrees.objects.create(
            user_id=self.profile,
            degree_id=self.degree
        )

    def test_test_view(self):
        assert 1 == 1

    def test_view_profile_view(self):
        response = self.client.post(self.view_profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')

    def test_edit_profile_view(self):
        response = self.client.post(self.edit_profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/edit_profile.html')

    def test_edit_privacy(self):
        response = self.client.get(self.edit_privacy_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/edit_privacy.html')

    def test_profile_user_matching(self):
        self.assertEqual(self.profile.user.username, 'testuser')
        self.assertEqual(self.profile.user, self.user)

    def test_profile_data_matching(self):
        self.assertNotEqual(self.course.course_id, '2')
        self.assertNotEqual(self.degree.degree_id, '2')
        self.assertEqual(self.userCourses.user_id, self.profile)
        self.assertEqual(self.userCourses.course_id, self.course)
        self.assertEqual(self.userDegrees.user_id, self.profile)
        self.assertEqual(self.userDegrees.degree_id, self.degree)
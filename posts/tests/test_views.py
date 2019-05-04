from django.contrib.auth.models import User
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from users.models import Profile, Privacy, Course, Degree, UserCourses, UserDegrees
from posts.models import Post
from django.views.generic import ListView


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

        # create user
        username = 'testuser'
        email = 'test@test.com'
        password = '12345'
        self.user = User(username=username, email=email)
        self.user.set_password(password)
        self.user.save()
        login = self.client.login(username=username, password=password)
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
            course_name='OOP'
        )
        self.degree = Degree.objects.create(
            degree_id='1',
            degree_name='Software Engineering'
        )
        self.userCourses = UserCourses.objects.create(
            user_id=self.profile,
            course_id=self.course
        )
        self.userDegrees = UserDegrees.objects.create(
            user_id=self.profile,
            degree_id=self.degree
        )

    def test_create_new_post_view(self):
        response = self.client.post(reverse('posts:newPost'))
        self.assertEqual(response.status_code, 200)

    def test_test_view(self):
        assert 1 == 1

    def test_publish_private_post(self):
        new_post = Post(category='other', body='unit test post', author=self.user)
        new_post.save()
        pk = new_post.id
        response = self.client.post(reverse('posts:post-detail', args=(pk,)))
        self.assertEqual(response.status_code, 200)

    def test_publish_study_post(self):
        new_post = Post(category='OOP', body='unit test post', author=self.user)
        new_post.save()
        pk = new_post.id
        response = self.client.post(reverse('posts:post-detail', args=(pk,)))
        self.assertEqual(response.status_code, 200)

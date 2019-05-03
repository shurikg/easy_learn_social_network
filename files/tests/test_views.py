
from coverage.annotate import os
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from files.models import File
from users.models import Course, Degree
from users.views import User
from django.utils import timezone


class TestUrls(TestCase):

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

        # create category
        self.category = Course.objects.create(
            course_id='1',
            course_name='OOP'
        )

        # create degree
        self.software_eng_degree = Degree.objects.create(
            degree_id='1',
            degree_name='Software Engineering'
        )

        self.social_worker_degree = Degree.objects.create(
            degree_id='2',
            degree_name='Social Worker'
        )

        # upload file
        f = SimpleUploadedFile('test.pdf', b'test context')

        # create file model object
        self.file1 = File(
            category=self.category,
            create_at=timezone.now,
            file_url=f,
            owner=self.user,
        )
        self.file1.save()
        self.file1.related_degrees.add(self.software_eng_degree)
        self.file1.related_degrees.add(self.social_worker_degree)

    def test_category_flow_view(self):
        category_name = self.category
        self.assertTrue(category_name, self.file1.category)

    def test_show_files_view(self):
        response = self.client.post(reverse('files:show_files'))
        self.assertEqual(response.status_code, 200)

    def test_show_files_view(self):
        response = self.client.post(reverse('files:show_files'))
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        os.remove(self.file1.file_url.path)


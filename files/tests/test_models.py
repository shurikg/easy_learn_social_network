import os

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.contrib.auth.models import User
from files.models import File as File
from users.models import Course, Degree
from django.utils import timezone


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

        # create category
        self.category = Course.objects.create(
            course_id='1',
            course_name='OOP'
        )

        # create degree
        self.software_eng = Degree.objects.create(
            degree_id='1',
            degree_name='Software Engineering'
        )

        self.statistic = Degree.objects.create(
            degree_id='2',
            degree_name='Statistic'
        )

        # upload file
        f = SimpleUploadedFile('test.pdf', b'test context')

        # create file model object
        self.file1 = File(
            category=self.category,
            create_at=timezone.now(),
            file_url=f,
            owner=self.user,
        )
        self.file1.save()
        self.file1.related_degrees.add(self.software_eng)
        self.file1.related_degrees.add(self.statistic)

    def test_file_extension(self):
        self.assertEqual(self.file1.file_type, 'pdf')

    def tearDown(self):
        os.remove(self.file1.file_url.path)

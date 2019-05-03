from django.test import TestCase
from files.models import File
from django.contrib.auth.models import User
from users.models import Course, Degree
import unittest.mock as mock
from files import models
from django.db import models as django_models


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

        # create course
        self.course = Course.objects.create(
            course_id='1',
            course_name='OOP'
        )

        # create degree
        self.degree = Degree.objects.create(
            degree_id='1',
            degree_name='Software Engineering'
        )

        self.file_mock = mock.MagicMock(spec=File)
        self.file_mock.name = 'test.pdf'

        self.file = File.objects.create(
            file_name='test_name',
            file_type='pdf',
            file_url=File(file_url=self.file_mock),
            # owner=self.user,
            # create_at=django_models.DateField(auto_now_add=True),
            # file_size='10',
            # category=self.course,
        )

        # self.file.related_degrees.set(self.degree)

    def test_file_exist(self):
        self.assertEqual(self.file.file_name, 'test_name')
        self.assertEqual(self.file.file_type, 'pdf')
        self.assertEqual(self.file_url.name, self.file_mock.name)
        #self.assertEqual(self.file.owner, 'test1')
        #self.assertEqual(self.file.create_at, '02/05/2019')
        #self.assertEqual(self.file.file_size, '10')
        #self.assertEqual(self.file.category, 'test1')
        #self.assertEqual(self.file.related_degrees, 'test1')
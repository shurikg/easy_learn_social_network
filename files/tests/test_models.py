import os

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.contrib.auth.models import User
from files.models import File
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
            create_at=timezone.now(),
            file_url=f,
            owner=self.user,
        )
        self.file1.save()
        self.file1.related_degrees.add(self.software_eng_degree)
        self.file1.related_degrees.add(self.social_worker_degree)

    def test_file_extension(self):
        self.assertEqual(self.file1.file_type, 'pdf')

    def test_name_start_with_id(self):
        file_id = str(self.file1.id)
        self.assertTrue(self.file1.file_name.startswith(file_id))

    def test_file_category(self):
        self.assertEqual(self.file1.category, self.category)

    def test_related_degrees(self):
        degrees = (self.social_worker_degree.degree_name, self.software_eng_degree.degree_name)
        for degree in self.file1.related_degrees.all():
            self.assertTrue(degree.degree_name in degrees)
        for degree_name in degrees:
            self.assertTrue(degree_name in (d.degree_name for d in self.file1.related_degrees.all()))

    def test_file_name_contains_owner(self):
        owner_username = self.user.username
        self.assertTrue(owner_username in self.file1.file_name)

    def test_owner(self):
        self.assertEqual(self.file1.owner, self.user)

    def test_upload_at(self):
        self.assertEqual(self.file1.upload_at.date(), timezone.now().date())

    def tearDown(self):
        os.remove(self.file1.file_url.path)

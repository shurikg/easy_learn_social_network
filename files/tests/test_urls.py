from coverage.annotate import os
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse, resolve
from files.models import File
from files.views import download_file, show_files, add_new_file
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
        try:
            self.file1.save()
        except FileExistsError as e:
            print(e)
        self.file1.related_degrees.add(self.software_eng_degree)
        self.file1.related_degrees.add(self.social_worker_degree)

    def test_add_file_url_is_resolved(self):
        url = reverse('files:add_file')
        self.assertEqual(resolve(url).func, add_new_file)

    def test_download_file_url_is_resolved(self):
        file_id = self.file1.id
        url = reverse('files:download_file', args=(file_id,))
        self.assertEqual(resolve(url).func, download_file)

    def test_file_is_resolved(self):
        file_id = self.file1.id
        url = reverse('files:show_files')
        self.assertNotEqual(resolve(url).func, download_file)

    def test_show_file_url_is_resolved(self):
        url = reverse('files:show_files')
        self.assertEqual(resolve(url).func, show_files)

    def test_file_flow(self):
        self.assertEqual(str(self.file1.category), 'OOP')
        self.assertEqual(str(self.file1.owner), self.user.username)
        self.assertEqual(str(self.file1.create_at.date()),  str(timezone.now().date()))
        self.assertEqual(self.file1.file_url.__str__(),  'files/1_testuser_OOP.pdf')

    def tearDown(self):
        try:
            os.remove(self.file1.file_url.path)
        except FileNotFoundError as e:
            print(e)

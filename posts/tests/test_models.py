from django.test import TestCase
from posts.models import Post, Comments
from django.contrib.auth.models import User
from users.models import Degree, Course
from files.models import File
from django.core.files.uploadedfile import SimpleUploadedFile
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

        # upload legal file
        self.legal = SimpleUploadedFile('test.pdf', b'test context')

        # create file model object
        self.legal_file = File(
            category=self.category,
            create_at=timezone.now(),
            file_url=self.legal,
            owner=self.user,
        )
        self.legal_file.save()
        self.legal_file.related_degrees.add(self.software_eng_degree)
        self.legal_file.related_degrees.add(self.social_worker_degree)

        # create post
        self.post1 = Post.objects.create(
            category='other',
            body='test1',
            author=self.user,
        )

        self.post2 = Post.objects.create(
            category='OOP',
            body='test2',
            author=self.user
        )

        # create post with file
        self.post3 = Post.objects.create(
            category='other',
            body='test3',
            author=self.user,
            file=self.legal_file
        )

        self.comment1 = Comments.objects.create(
            comment='comment1',
            postId=self.post1,
            author=self.user
        )

        self.comment2 = Comments.objects.create(
            comment='comment2',
            postId=self.post2,
            author=self.user
        )

    def test_post_with_file_exist(self):
        self.assertEqual(self.post3.category, 'other')
        self.assertEqual(self.post3.body, 'test3')
        self.assertEqual(str(self.post3.file.category), 'OOP')
        self.assertEqual(self.post3.file.create_at.date(), timezone.now().date())
        self.assertEqual(self.post3.file.file_url, 'files/1_testuser_OOP.pdf')
        self.assertEqual(self.post3.file.owner, self.user)

    def test_post_Other_exist(self):
        self.assertEqual(self.post1.category, 'other')
        self.assertEqual(self.post1.body, 'test1')

    def test_post_Study_exist(self):
        self.assertEqual(self.post2.category, 'OOP')
        self.assertEqual(self.post2.body, 'test2')

    def test_post_not_exist(self):
        self.assertNotEqual(self.post1.category, 'other1')
        self.assertNotEqual(self.post1.body, 'test11')

    def test_comment_exist(self):
        self.assertEqual(self.comment1.comment, 'comment1')

    def test_get_only_post_comment(self):
        comments = Comments.objects.filter(postId=self.post1)
        for comment in comments:
            self.assertEqual(comment.postId.id, self.post1.id)

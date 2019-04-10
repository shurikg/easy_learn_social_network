from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    category = models.CharField(max_length=50)
    body = models.TextField(max_length=5000)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.category


class Comments(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(max_length=5000)
    postId = models.ForeignKey(Post, on_delete=models.CASCADE)
    publish_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{0}-{1}'.format(self.postId.category, str(self.author.username))

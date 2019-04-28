from django.db import models
from django.contrib.auth.models import User


class File(models.Model):
    file_name = models.CharField(max_length=30, default='')
    file_type = models.CharField(max_length=10, default='')
    file_url = models.FileField(upload_to='files/', default='')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    create_at = models.DateTimeField()
    upload_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file_name

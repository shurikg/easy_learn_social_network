from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from users.models import Course, Degree
import os


class File(models.Model):
    file_name = models.CharField(max_length=30, null=True, blank=True)
    file_type = models.CharField(max_length=10, null=True, blank=True)
    file_url = models.FileField(upload_to='files/', default='')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    create_at = models.DateField(null=True)
    upload_at = models.DateTimeField(auto_now_add=True)
    file_size = models.DecimalField(max_digits=27, decimal_places=2, null=True, blank=True)
    category = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    related_degrees = models.ManyToManyField(Degree, blank=True)

    def __str__(self):
        return self.file_name

    def get_file_extension(self):
        name, extension = os.path.splitext(self.file_url.name)
        return str(extension)

    def save(self, **kwargs):
        if not self.id:
            self.create_at = timezone.now()
        super(File, self).save(**kwargs)

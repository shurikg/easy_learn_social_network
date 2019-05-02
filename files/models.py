from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from EasyLearn import settings
from users.models import Course, Degree
import os


UPLOAD_TO_DIR = 'files/'


class File(models.Model):
    file_name = models.CharField(max_length=30, null=True, blank=True)
    file_type = models.CharField(max_length=10, null=True, blank=True)
    file_url = models.FileField(upload_to=UPLOAD_TO_DIR, default='')
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
        return str(extension)[1:]  # remove the '.'

    def save(self, **kwargs):
        if not self.id:
            self.create_at = timezone.now()
        super(File, self).save(**kwargs)
        initial_path = self.file_url.path
        self.file_type = self.get_file_extension()
        self.file_name = '' + str(self.id) + '.' + str(self.file_type)
        new_path = settings.MEDIA_ROOT + '/' + UPLOAD_TO_DIR + self.file_name
        os.rename(initial_path, new_path)
        super(File, self).save(**kwargs)

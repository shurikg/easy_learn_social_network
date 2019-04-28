from django.db import models
from django.contrib.auth.models import User
from users.models import Course, Degree


class File(models.Model):
    file_name = models.CharField(max_length=30, null=True, blank=True)
    file_type = models.CharField(max_length=10, null=True, blank=True)
    file_url = models.FileField(upload_to='files/', default='')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    create_at = models.DateTimeField(null=True)
    upload_at = models.DateTimeField(auto_now_add=True)
    file_size = models.DecimalField(max_digits=27, decimal_places=2, null=True, blank=True)
    category = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    related_degrees = models.ManyToManyField(Degree, blank=True)

    def __str__(self):
        return self.file_name

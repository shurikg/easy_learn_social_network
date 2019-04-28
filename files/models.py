from django.db import models


class File(models.Model):
    file_name = models.CharField(max_length=30, default='')
    file_type = models.CharField(max_length=10, default='')
    file_url = models.FileField(upload_to='files/', default='')

    def __str__(self):
        return self.file_name

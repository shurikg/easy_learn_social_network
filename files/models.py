from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from EasyLearn import settings
from users.models import Course, Degree
import os
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from django.dispatch import receiver
import uuid
from django.utils.translation import ugettext_lazy as _

EXTENSIONS_WHITELIST = ('pdf', 'docx', 'doc', 'jpg', 'png', 'jpeg', 'txt', 'zip', 'rar')
UPLOAD_TO_DIR = 'files/'


class File(models.Model):
    file_name = models.CharField(max_length=30, null=True, blank=True)
    file_type = models.CharField(max_length=10, null=True, blank=True)
    file_url = models.FileField(upload_to=UPLOAD_TO_DIR, default='')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    create_at = models.DateField(null=True)
    upload_at = models.DateTimeField(auto_now_add=True)
    file_size = models.CharField(max_length=10, null=True, blank=True)
    category = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    related_degrees = models.ManyToManyField(Degree, blank=True)

    def __str__(self):
        return str(self.file_name)

    def get_file_extension(self):
        name, extension = os.path.splitext(self.file_url.name)
        return str(extension)[1:]  # remove the '.'

    def get_file_size(self):
        size_in_bytes = self.file_url.size
        if 0 < size_in_bytes < 1024:
            return '{0} B'.format(size_in_bytes)
        elif 1024 <= size_in_bytes < 1024**2:
            return '{0:.2f} KB'.format(size_in_bytes / 1024)
        else:
            return '{0:.2f} MB'.format(size_in_bytes / (1024**2))

    def get_str_of_related_degrees(self):
        output = ''
        for degree in self.related_degrees.all():
            output += degree.degree_name + ', '
        return output[:-2]

    def save(self, **kwargs):
        extension = self.get_file_extension()
        if extension not in EXTENSIONS_WHITELIST:
            raise ValidationError('The file extension is not allowed')
        if not self.id:
            self.create_at = timezone.now()
        self.file_size = self.get_file_size()
        super(File, self).save(**kwargs)
        initial_path = self.file_url.path
        self.file_type = self.get_file_extension()
        owner_username = str(self.owner).replace(' ', '')
        file_category = str(self.category).replace(' ', '')
        self.file_name = '' + str(self.id) + '_' + owner_username + '_' + file_category + '.' + str(self.file_type)
        new_path = settings.MEDIA_ROOT + '/' + UPLOAD_TO_DIR + self.file_name
        os.rename(initial_path, new_path)
        self.file_url.name = os.path.join(UPLOAD_TO_DIR, self.file_name)
        super(File, self).save(**kwargs)


    #@receiver(models.signals.post_delete, sender=File)
    #def auto_delete_file_on_delete(sender, instance, **kwargs):
        """
        Deletes file from filesystem
        when corresponding `MediaFile` object is deleted.
        """
        #if instance.file_url:
            #if os.path.isfile(instance.file_url.path):

                #os.remove(instance.file_url.path)

    #@receiver(pre_delete, sender=File)
    #def mymodel_delete(sender, instance, **kwargs):
        #'''Pass false so FileField doesn't save the model.'''
        #instance.file.delete(False)

    #def delete(self, using=None, keep_parents=False):
        #os.remove(self.legal_file.file_url.path)
        #super(File, self).delete(self)


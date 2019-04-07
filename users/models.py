from django.core.validators import MaxValueValidator
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    birth_date = models.DateField(default='')
    gender = models.CharField(max_length=10)
    college_name = models.CharField(max_length=50)
    year_of_study = models.PositiveIntegerField(validators=[MaxValueValidator(10)])
    about_me = models.TextField(max_length=250, null=True, blank=True, default='')

    def __str__(self):
        return str(self.user)


class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.course_name


class Degree(models.Model):
    degree_id = models.AutoField(primary_key=True)
    degree_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.degree_name


class UserCourses(models.Model):
    user_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return '{0}, {1}'.format(str(self.user_id), str(self.course_id))

    class Meta:
        unique_together = ('user_id', 'course_id',)


class UserDegrees(models.Model):
    user_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    degree_id = models.ForeignKey(Degree, on_delete=models.CASCADE)

    def __str__(self):
        return '{0}, {1}'.format(str(self.user_id), str(self.degree_id))

    class Meta:
        unique_together = ('user_id', 'degree_id',)



#
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#
#
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()

from django.contrib import admin

from .models import *

admin.site.register(Degree)
admin.site.register(Course)
admin.site.register(Profile)
admin.site.register(UserDegrees)
admin.site.register(UserCourses)
admin.site.register(Privacy)
admin.site.register(FriendRequest)


from django import forms
from posts.models import Post, Comments
from users.models import Course

OTHER_CATEGORY = 'other'


class SelectCategoryForm(forms.ModelForm):
    CATEGORY_CHOICES = (
        (OTHER_CATEGORY, 'Other'),
    )
    COURSES = ()
    try:
        COURSES = tuple(map(lambda course_name: (course_name, course_name), Course.objects.only('course_name')))
    except Exception as e:
        print(e)
    category_list = CATEGORY_CHOICES + COURSES

    category = forms.ChoiceField(choices=category_list,required=False)

    class Meta:
        model = Post
        fields = ('category',)

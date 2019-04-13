from django import forms
from posts.models import Post, Comments
from users.models import Course


class NewPost(forms.ModelForm):
    CATEGORY_CHOICES = (
        ('other', 'Other'),
    )
    COURSES = tuple(map(lambda course_name: (course_name, course_name), Course.objects.only('course_name')))
    category_list = CATEGORY_CHOICES + COURSES

    category = forms.ChoiceField(help_text='Select category', choices=category_list)
    body = forms.CharField(max_length=5000, widget=forms.Textarea)

    class Meta:
        model = Post
        fields = ('category', 'body',)


class Comment(forms.ModelForm):
    comment = forms.CharField(max_length=5000, widget=forms.TextInput(attrs={'placeholder': 'write comment...'}))

    class Meta:
        model = Comments
        fields = ('comment',)

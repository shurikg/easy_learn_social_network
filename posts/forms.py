from django import forms
from posts.models import Post, Comments
from users.models import Course

OTHER_CATEGORY = 'other'


class NewPost(forms.ModelForm):
    CATEGORY_CHOICES = (
        (OTHER_CATEGORY, 'Other'),
    )
    COURSES = tuple(map(lambda course_name: (course_name, course_name), Course.objects.only('course_name')))
    category_list = CATEGORY_CHOICES + COURSES

    category = forms.ChoiceField(help_text='By selecting the "Other" option, only your friends can view the post. ' +
                                           'Otherwise the post will be set to public.', choices=category_list)
    body = forms.CharField(max_length=5000, widget=forms.Textarea)

    class Meta:
        model = Post
        fields = ('category', 'body',)


class Comment(forms.ModelForm):
    comment = forms.CharField(max_length=5000, widget=forms.TextInput(attrs={'placeholder': 'write comment...'}))

    class Meta:
        model = Comments
        fields = ('comment',)

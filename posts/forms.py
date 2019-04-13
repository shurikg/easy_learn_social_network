from django import forms
from posts.models import Post, Comments
from users.models import Course


class NewPost(forms.ModelForm):
    CATEGORY_CHOICES = (
        ('other', 'Other'),
        ('study', 'Study'),
    )

    item_field = forms.ModelChoiceField(queryset=Course.objects.only('course_name'))

    # def __init__(self):
    #     super(NewPost, self).__init__()
    #     self.fields['item_field'].queryset = Course.objects.filter(course_name=)

    category = forms.ChoiceField(help_text='Select category', choices=CATEGORY_CHOICES)
    body = forms.CharField(max_length=5000, widget=forms.Textarea)

    class Meta:
        model = Post
        fields = ('category', 'item_field', 'body',)


class Comment(forms.ModelForm):
    comment = forms.CharField(max_length=5000, widget=forms.TextInput(attrs={'placeholder': 'write comment...'}))

    class Meta:
        model = Comments
        fields = ('comment',)

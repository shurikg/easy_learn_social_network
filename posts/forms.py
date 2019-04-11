from django import forms
from posts.models import Post, Comments


class NewPost(forms.ModelForm):
    CATEGORY_CHOICES = (
        ('other', 'Other'),
        ('study', 'Study'),
    )

    category = forms.ChoiceField(help_text='Select category', choices=CATEGORY_CHOICES)
    body = forms.CharField(max_length=5000, widget=forms.Textarea)

    class Meta:
        model = Post
        fields = ('category', 'body',)


class Comment(forms.ModelForm):
    comment = forms.CharField(max_length=5000, widget=forms.TextInput(attrs={'placeholder': 'write comment...'}))

    class Meta:
        model = Comments
        fields = ('comment',)

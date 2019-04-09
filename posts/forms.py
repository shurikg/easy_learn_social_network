from django import forms
from posts.models import Post


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

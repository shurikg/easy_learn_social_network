from django import forms
from posts.models import Post, Comments
from users.models import Course

OTHER_CATEGORY = 'other'
FIELD_NAME_MAPPING = {
    'category': 'post_type'
}


class NewPostForm(forms.ModelForm):
    CATEGORY_CHOICES = (
        (OTHER_CATEGORY, 'Other'),
    )
    COURSES = ()
    try:
        COURSES = tuple(map(lambda course_name: (course_name, course_name), Course.objects.only('course_name')))
    except Exception as e:
        print(e)
    category_list = CATEGORY_CHOICES + COURSES
    category_rules = 'By selecting the "Other" option, only your friends can view the post. ' \
                     'Otherwise the post will be set to public.'

    category = forms.ChoiceField(help_text=category_rules, choices=category_list)
    body = forms.CharField(max_length=5000, widget=forms.Textarea)

    def add_prefix(self, field_name):
        # look up field name; return original if not found
        field_name = FIELD_NAME_MAPPING.get(field_name, field_name)
        return super(NewPostForm, self).add_prefix(field_name)

    class Meta:
        model = Post
        fields = ('category', 'body',)


class Comment(forms.ModelForm):
    comment = forms.CharField(max_length=250,
                              widget=forms.TextInput(attrs={'placeholder': 'write comment...'}),
                              help_text='Please write your comment (maximum 250 characters)')

    class Meta:
        model = Comments
        fields = ('comment', )

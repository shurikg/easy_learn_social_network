from django import forms
from django.core.exceptions import ValidationError

from files.models import File
from users.models import Course, Degree


class DateInput(forms.DateInput):
    input_type = 'date'


EXTENSIONS_WHITELIST = ('pdf', 'docx', 'doc', 'jpg', 'png', 'jpeg', 'txt', 'zip', 'rar')


class CreateNewFileForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Course.objects.all())
    related_degrees = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                                     queryset=Degree.objects.all(),
                                                     error_messages={'required': 'You must select at least one degree.'})
    create_at = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = File
        fields = ('category', 'related_degrees', 'create_at', 'file_url',)

    def clean_file_url(self):
        file = self.cleaned_data.get('file_url')
        if file:
            filename = file.name
            if filename.split('.')[-1] not in EXTENSIONS_WHITELIST:
                self.add_error('file_url', 'The file extension is not allowed.')
                # raise ValidationError('The file extension is not allowed.')
        return file


OTHER_CATEGORY = 'other'


class categoryForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Course.objects.all(),required=False)

    class Meta:
        model = File
        fields = ('category',)

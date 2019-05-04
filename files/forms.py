from django import forms

from files.models import File, EXTENSIONS_WHITELIST
from users.models import Course, Degree
from users.views import User

FIELD_NAME_MAPPING = {
    'category': 'file_type'
}


class DateInput(forms.DateInput):
    input_type = 'date'


class CreateNewFileForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Course.objects.all())
    related_degrees = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                                     queryset=Degree.objects.all(),
                                                     error_messages={'required': 'You must select at least one degree.'})
    create_at = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))

    def add_prefix(self, field_name):
        # look up field name; return original if not found
        field_name = FIELD_NAME_MAPPING.get(field_name, field_name)
        return super(CreateNewFileForm, self).add_prefix(field_name)

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


class filterFilesForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Course.objects.all(), required=False)
    degree = forms.ModelChoiceField(queryset=Degree.objects.all(), required=False)
    user = forms.ModelChoiceField(queryset=User.objects.all(), required=False)

    class Meta:
        model = File
        fields = ('category', 'degree', 'user')

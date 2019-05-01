from django import forms
from files.models import File
from users.models import Course, Degree


class DateInput(forms.DateInput):
    input_type = 'date'


class CreateNewFile(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Course.objects.all())
    related_degrees = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=Degree.objects.all())
    create_at = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = File
        fields = ('category', 'related_degrees', 'create_at',)

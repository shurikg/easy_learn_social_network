from django import forms
from files.models import File
from users.models import Course, Degree


class DateInput(forms.DateInput):
    input_type = 'date'


class CreateNewFile(forms.ModelForm):
    COURSES = ()
    DEGREES = ()
    try:
        COURSES = tuple(map(lambda course_name: (course_name, course_name), Course.objects.only('course_name')))
        DEGREES = tuple(map(lambda degree: (degree, degree), Degree.objects.only('degree_name')))
    except Exception as e:
        print(e)

    category = forms.ChoiceField(choices=COURSES)
    related_degrees = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=DEGREES)
    create_at = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    file_url = forms.FileField(label='File')

    class Meta:
        model = Course
        fields = ('category', 'related_degrees', 'create_at', 'file_url',)

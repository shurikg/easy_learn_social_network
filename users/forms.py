from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from users.models import Profile, UserCourses, UserDegrees


class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email']


class NewUserProfileForm(forms.ModelForm):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )
    birth_date = forms.DateField(help_text='Enter date in format mm/dd/yyyy.')
    gender = forms.ChoiceField(help_text='Select your gender', choices=GENDER_CHOICES)
    college_name = forms.CharField(max_length=50, help_text='Enter your collage name.')
    year_of_study = forms.ChoiceField(choices=[(x, x) for x in range(1, 7)])
    about_me = forms.CharField(max_length=250, help_text='Tell something about you (max 250 characters).')

    class Meta:
        model = Profile
        fields = {'birth_date', 'gender', 'college_name', 'year_of_study', 'about_me'}


class NewUserDegreeForm(forms.ModelForm):
    degree = forms.CharField(max_length=20,
                             help_text='If your degree is not listed, you can ask the administrator to add it')

    class Meta:
        model = UserDegrees
        fields = {'degree'}


class NewUserCourseForm(forms.ModelForm):
    course = forms.CharField(max_length=20,
                             help_text='If your course is not listed, you can ask the administrator to add it')

    class Meta:
        model = UserCourses
        fields = {'course'}

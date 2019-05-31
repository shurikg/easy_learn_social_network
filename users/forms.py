from coverage.files import os
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from users.models import Profile, UserCourses, UserDegrees, Privacy
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from EasyLearn.settings import MEDIA_ROOT
from .models import GENDER_CHOICES, Degree, Course


class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email']


class NewUserProfileForm(forms.ModelForm):
    birth_date = forms.DateField(help_text='Enter date in format mm/dd/yyyy.',
                                 widget=forms.widgets.DateInput(attrs={'type': 'date'}),)
    gender = forms.ChoiceField(help_text='Select your gender', choices=GENDER_CHOICES)
    college_name = forms.CharField(max_length=50, help_text='Enter your collage name.')
    year_of_study = forms.ChoiceField(choices=[(x, x) for x in range(1, 8)])
    about_me = forms.CharField(max_length=250, help_text='Tell something about you (max 250 characters).',
                               required=False)
    profile_pic = forms.ImageField(required=True, widget=forms.FileInput)

    class Meta:
        model = Profile
        fields = {'birth_date', 'gender', 'college_name', 'year_of_study', 'about_me', 'profile_pic'}

    def save(self, commit=True):
        instance = super(NewUserProfileForm, self).save(commit=False)
        new_pic_name = '{0}_profile_pic.jpg'.format(instance.user.username)
        instance.profile_pic.name = new_pic_name
        if commit:
            instance.save()
        return instance


class NewUserDegreeForm(forms.ModelForm):
    degree = forms.ModelChoiceField(queryset=Degree.objects.all()
                                    , help_text='If your degree is not listed, you can ask the administrator to add it')

    class Meta:
        model = UserDegrees
        fields = {'degree'}


class NewUserCourseForm(forms.ModelForm):
    course = forms.ModelMultipleChoiceField(queryset=Course.objects.all(),
                                            help_text='You can select many corses by clicking on ctrl key and select '
                                                      'the course with the mouse.\n'
                                                      'If your course is not listed, you can ask the '
                                                      'administrator to add it',)

    class Meta:
        model = UserCourses
        fields = {'course'}


class LoginForm(AuthenticationForm):
    username = UsernameField(max_length=50, widget=forms.TextInput(attrs={'autofocus': True,
                                                                          'placeholder': 'Enter user name here'}))
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter password here'}),
    )

    class Meta:
        model = User
        fields = {'username', 'password'}


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
        )


class EditPersonalInfoForm(forms.ModelForm):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )
    birth_date = forms.DateField(help_text='Enter date in format mm/dd/yyyy.')
    gender = forms.ChoiceField(help_text='Select your gender', choices=GENDER_CHOICES)

    class Meta:
        model = Profile
        fields = ('gender', 'birth_date',)


class EditMoreInfoForm(forms.ModelForm):
    college_name = forms.CharField(max_length=50, help_text='Enter your collage name.')
    year_of_study = forms.ChoiceField(choices=[(x, x) for x in range(1, 7)])
    about_me = forms.CharField(max_length=250, help_text='Tell something about you (max 250 characters).',
                               widget=forms.Textarea)
    profile_pic = forms.ImageField(required=False, widget=forms.FileInput)
    remove_profile_picture = forms.BooleanField(required=False)

    class Meta:
        model = Profile
        fields = ('college_name', 'year_of_study', 'about_me', 'profile_pic')

    def save(self, commit=True):
        old_pic_name = '{0}_profile_pic.jpg'.format(self.instance.user.username)
        try:
            os.remove('{0}/profilepics/{1}'.format(MEDIA_ROOT, old_pic_name))
        except FileNotFoundError as e:
            print(e)
        instance = super(EditMoreInfoForm, self).save(commit=False)

        instance.profile_pic.name = old_pic_name

        if self.cleaned_data.get('remove_profile_picture'):
            try:
                if instance.profile_pic:
                    os.unlink(instance.profile_pic.path)
            except OSError:
                pass
            instance.profile_pic = None
        if commit:
            instance.save()
        return instance


class PasswordAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = (
            'password'
        )


class EditPrivacyForm(forms.ModelForm):
    privacy_first_name = forms.BooleanField(label='first name', required=False)
    privacy_last_name = forms.BooleanField(label='last name', required=False)
    privacy_email = forms.BooleanField(label='email', required=False)
    privacy_birth_date = forms.BooleanField(label='birth day', required=False)
    privacy_gender = forms.BooleanField(label='gender', required=False)
    privacy_college_name = forms.BooleanField(label='college name', required=False)
    privacy_year_of_study = forms.BooleanField(label='year of study', required=False)
    privacy_about_me = forms.BooleanField(label='about me', required=False)

    class Meta:
        model = Privacy
        fields = (
            'privacy_first_name',
            'privacy_last_name',
            'privacy_email',
            'privacy_birth_date',
            'privacy_gender',
            'privacy_college_name',
            'privacy_year_of_study',
            'privacy_about_me',
        )


class ExtraProfileForm(forms.ModelForm):

    def __init__(self, privacy_obj, *args, **kwargs):
        super(ExtraProfileForm, self).__init__(*args, **kwargs)
        self.privacy_obj = privacy_obj

        if self.privacy_obj.privacy_gender:
            self.fields['gender'] = forms.CharField()
        if self.privacy_obj.privacy_birth_date:
            self.fields['birth_date'] = forms.CharField()
        if self.privacy_obj.privacy_college_name:
            self.fields['college_name'] = forms.CharField()
        if self.privacy_obj.privacy_year_of_study:
            self.fields['year_of_study'] = forms.CharField()
        if self.privacy_obj.privacy_about_me:
            self.fields['about_me'] = forms.CharField()

    class Meta:
        model = Profile
        fields = ()


class ProfileForm(forms.ModelForm):
    def __init__(self, privacy_obj, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.privacy_obj = privacy_obj

        if self.privacy_obj.privacy_first_name:
            self.fields['first_name'] = forms.CharField()
        if self.privacy_obj.privacy_last_name:
            self.fields['last_name'] = forms.CharField()
        if self.privacy_obj.privacy_email:
            self.fields['email'] = forms.CharField()

    class Meta:
        model = User
        fields = ()

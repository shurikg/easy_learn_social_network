from django.core import serializers
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, NewUserProfileForm, NewUserDegreeForm, NewUserCourseForm
from formtools.wizard.views import SessionWizardView
from django.contrib.auth.models import User
from .models import Profile, UserDegrees, UserCourses, Course, Degree


def register(request):
    if request.method == 'POST':
        registration_form = UserRegisterForm(request.POST)
        if registration_form.is_valid():
            registration_form.save()
            username = registration_form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('users.view.add_profile_detail')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        registration_form = UserRegisterForm()
    return render(request, 'users/register.html', {'registration_form': registration_form, })


def add_profile_detail(request):
    return render(request, 'users/add_user_detail.html')
    # if request.method == 'POST':
    #     registration_form = UserRegisterForm(request.POST)
    #     personal_data_form = UserProfileForm(request.POST)
    #     if registration_form.is_valid() and personal_data_form.is_valid():
    #         registration_form.save()
    #         personal_data_form.save()
    #         username = registration_form.cleaned_data.get('username')
    #         messages.success(request, f'Account created for {username}!')
    #         return redirect('add_user_detail')
    #     else:
    #         messages.error(request, 'Please correct the error below.')
    # else:  # GET request, at the first time, when the user want to register with an empty form
    #     registration_form = UserRegisterForm()
    #     personal_data_form = UserProfileForm()
    # return render(request, 'users/register.html',
    #               {'registration_form': registration_form,
    #                'personal_data_form': personal_data_form
    #                })


class RegisterFormWizard(SessionWizardView):
    template_name = "users/wiz.html"
    form_list = [UserRegisterForm, NewUserProfileForm, NewUserDegreeForm, NewUserCourseForm]
    # form_list = [UserDegreeForm]

    def done(self, form_list, **kwargs):
        forms_dict = {}
        for form in form_list:
            forms_dict[type(form)] = form

        user = forms_dict[UserRegisterForm].save()

        profile = forms_dict[NewUserProfileForm].save(commit=False)
        profile.user = user
        profile.save()

        user_degree = forms_dict[NewUserDegreeForm].save(commit=False)
        user_degree.user_id = profile
        form_degree_name = forms_dict[NewUserDegreeForm].cleaned_data.get('degree')
        degree = Degree.objects.get(degree_name=form_degree_name)
        user_degree.degree_id = degree
        user_degree.save()

        user_course = forms_dict[NewUserCourseForm].save(commit=False)
        user_course.user_id = profile
        form_course_name = forms_dict[NewUserCourseForm].cleaned_data.get('course')
        course = Course.objects.get(course_name=form_course_name)
        user_course.course_id = course
        user_course.save()

        return render(self.request, 'users/test.html')


# def test(request):
#     x = Degree.objects.values()
#     x = [(entry['degree_id'], entry['degree_name']) for entry in x]
#
#     x = Degree.objects.values()
#     x = [(entry['degree_id'], entry['degree_name']) for entry in x]
#     x = Degree.objects.all()
#     x = serializers.serialize('json', x)
#     print(x)
#
#     x = Degree.objects.all()
#     x = serializers.serialize('json', x)
#     print(x)
#     return render(request, 'users/test.html')

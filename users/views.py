#from django.contrib.gis.gdal.prototypes.srs import from_user_input
from django.core import serializers
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import UserRegisterForm, NewUserProfileForm, NewUserDegreeForm, NewUserCourseForm, LoginForm, ProfileForm
from formtools.wizard.views import SessionWizardView
from django.contrib.auth.models import User
from .models import Profile, UserDegrees, UserCourses, Course, Degree, Privacy, FriendRequest, Rules
from django.urls import reverse
from django.contrib.auth import authenticate, update_session_auth_hash, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.db.models import Q
from .forms import (
    EditProfileForm,
    PasswordAuthenticationForm,
    EditPersonalInfoForm,
    EditMoreInfoForm,
    ExtraProfileForm,
    EditPrivacyForm
)
from django.core.paginator import Paginator

User = get_user_model()

# def register(request):
#     if request.method == 'POST':
#         registration_form = UserRegisterForm(request.POST)
#         if registration_form.is_valid():
#             registration_form.save()
#             username = registration_form.cleaned_data.get('username')
#             messages.success(request, f'Account created for {username}!')
#             return redirect('users.view.add_profile_detail')
#         else:
#             messages.error(request, 'Please correct the error below.')
#     else:
#         registration_form = UserRegisterForm()
#     return render(request, 'users/register.html', {'registration_form': registration_form, })


class RegisterFormWizard(SessionWizardView):
    template_name = "users/register_wizard.html"
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

        privacy = Privacy()
        privacy.save()

        messages.success(self.request, f'Registration successful!')
        return redirect(reverse('home'))

# def login_page(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             return render(request, 'users/profile.html', {"user": username})
#         else:
#             messages.error(request, 'Invalid user name or password!')
#     else:
#         form = LoginForm()
#     return render(request, 'users/login.html', {"form": form})


def home_page(request):
    return render(request, 'users/home.html')


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

'''
@login_required
def view_profile(request):
    user_obj = request.user
    profile_obj = Profile.objects.get(user=user_obj)
    args = {'user': user_obj, 'profile': profile_obj}
    return render(request, 'users/profile.html', args)
'''


@login_required
def view_profile(request):
    user_obj = request.user
    profile_obj = Profile.objects.get(user=user_obj)
    friend_requests_obj = FriendRequest.objects.filter(to_user=request.user)
    args = {'user': user_obj,
            'profile': profile_obj,
            'friend_requests': friend_requests_obj}
    return render(request, 'users/profile.html', args)


@login_required
def edit_personal_info(request):
    profile_obj = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        u_form = EditPersonalInfoForm(request.POST, instance=profile_obj)
        p_form = EditProfileForm(request.POST, instance=request.user)
        chk_pass = PasswordAuthenticationForm(request, data=request.POST)
        if u_form.is_valid() and p_form.is_valid():
            if chk_pass.is_valid():
                username = chk_pass.cleaned_data.get('username')
                password = chk_pass.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    # profile = u_form.save(commit=False)
                    # profile.user = user
                    # profile.save()
                    # birthday = u_form.cleaned_data.get('birth_date')
                    # gender = u_form.cleaned_data.get('gender')

                    # user = Profile.objects.get(user_id=1)
                    # user.birth_date = birthday  # change field
                    # user.gender = gender  # change field
                    # user.save()  # this will update only
                    # p_form.save()
                    # u_form.save()

                    p_form.save()
                    u_form.save()

                    messages.success(request, f'Your account has been updated!')
                    return redirect(reverse('users:view_profile'))
            else:
                messages.error(request, f'Invalid password!')
        else:
            messages.error(request, f'Invalid fields, your account has not been updated!')

    else:
        u_form = EditPersonalInfoForm(instance=profile_obj)
        p_form = EditProfileForm(instance=request.user)
        chk_pass = PasswordAuthenticationForm()
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'chk_pass': chk_pass
    }

    return render(request, 'users/edit_personal_info.html', context)


@login_required
def edit_more_info(request):
    profile_obj = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form = EditMoreInfoForm(request.POST, instance=profile_obj)

        if form.is_valid():
            # profile = form.save(commit=False)
            # profile.user = request.user
            # profile.save()

            # id = form.cleaned_data.get('id')
            # collageName = form.cleaned_data.get('collageName')
            # yearOfStudy = form.cleaned_data.get('yearOfStudy')
            # aboutMe = form.cleaned_data.get('aboutMe')

            # user = Profile.objects.get(id=request.user.id)
            # user.id = id  # change field
            # user.collageName = collageName  # change field
            # user.yearOfStudy = yearOfStudy  # change field
            # user.aboutMe = aboutMe  # change field

            # user.save()  # this will update only
            form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('users:view_profile')
        else:
            messages.error(request, f'Invalid fields, your account has not been updated!')

    else:
        form = EditMoreInfoForm(instance=profile_obj)
    context = {
        'form': form,
    }
    return render(request, 'users/edit_more_info.html', context)


@login_required
def edit_profile(request):
    messages.info(request, 'what would you like to edit?')
    return render(request, 'users/edit_profile.html')


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, f'Password has been updated for {form.user}!')
            return redirect(reverse('users:view_profile'))
        else:
            messages.error(request, f'Password has not been updated for {form.user}!')
            return redirect(reverse('users:change_password'))

    else:
        form = PasswordChangeForm(user=request.user)

        args = {'form': form}
        return render(request, 'users/change_password.html', args)


@login_required
def show_users(request):
    users = User.objects.all()
    args = {'users': users}
    return render(request, 'users/search_users.html', args)

'''
def show_selected_user(request):
    user_id = request.GET.get('user_id')
    user = User.objects.get(id=user_id)

    profile_obj = Profile.objects.get(user=user)
    privacy_obj = Privacy.objects.get(user=user)

    extra_form = ExtraProfileForm(instance=profile_obj, privacy_obj=privacy_obj)
    profile_form = ProfileForm(instance=user, privacy_obj=privacy_obj)

    context = {
        'extra_form': extra_form,
        'profile_form': profile_form,
    }
    return render(request, 'users/show_selected_user.html', context)
'''


@login_required
def show_selected_user(request, id):
    user = get_object_or_404(User, id=id)

    profile_obj = Profile.objects.get(user=user)
    privacy_obj = Privacy.objects.get(user=user)

    extra_form = ExtraProfileForm(instance=profile_obj, privacy_obj=privacy_obj)
    profile_form = ProfileForm(instance=user, privacy_obj=privacy_obj)

    sent_friend_request = FriendRequest.objects.filter(from_user=user)

    friend_status = 'friends'
    if profile_obj not in request.user.profile.friends.all():
        friend_status = 'not_friend'
        if len(FriendRequest.objects.filter(from_user=request.user).filter(to_user=user)) == 1:
            friend_status = 'friend_request_sent'

    context = {
        'extra_form': extra_form,
        'profile_form': profile_form,
        'user': user,
        'sent_friend_request': sent_friend_request,
        'button_status': friend_status
    }
    return render(request, 'users/show_selected_user.html', context)


'''
def show_selected_user(request, slug):
    user_id = request.GET.get('user_name')
    user = User.objects.get(id=user_id)

    profile_obj = Profile.objects.get(user=user)
    privacy_obj = Privacy.objects.get(user=user)

    extra_form = ExtraProfileForm(instance=profile_obj, privacy_obj=privacy_obj)
    profile_form = ProfileForm(instance=request.user, privacy_obj=privacy_obj)

    other_profile = Profile.objects.filter(slug=slug).first()
    u = other_profile.user
    sent_friend_request = FriendRequest.objects.filter(from_user=other_profile.user)

    button_status = 'none'
    if other_profile not in request.user.profile.friends.all():
        button_status = 'not_friend'
        if len(FriendRequest.objects.filter(from_user = request.user).filter(to_user=other_profile.user)) == 1:
            button_status = 'friend_request_sent'

    context = {
        'extra_form': extra_form,
        'profile_form': profile_form,
        'u': u,
        'sent_friend_request': sent_friend_request,
        'button_status': button_status
    }
    #return render(request, 'users/show_selected_user.html/{}'.format(request.user.profile.slug), context)
    return render(request, 'users/show_selected_user.html', context)
'''


@login_required
def search_result(request):
    query = request.GET.get('q')
    if query:
        users = User.objects.filter(Q(first_name=query) | Q(last_name=query))
    else:
        users = User.objects.all()
    args = {'users': users}
    return render(request, 'users/search_users.html', args)


@login_required
def edit_privacy(request):
    privacy_obj = Privacy.objects.get(user=request.user)

    if request.method == 'POST':
        form = EditPrivacyForm(request.POST, instance=privacy_obj)

        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('users:view_profile')
        else:
            messages.error(request, f'Invalid fields, your account has not been updated!')

    else:
        form = EditPrivacyForm(instance=privacy_obj)
    context = {
        'form': form,
    }
    return render(request, 'users/edit_privacy.html', context)


# @login_required
# def test1(request):
#     #user_id = request.GET.get('user_name')
#     #user = User.objects.get(id=user_id)
#
#     profile_obj = Profile.objects.get(user=request.user)
#     privacy_obj = Privacy.objects.get(user=request.user)
#
#     #profile_obj = Profile.objects.get(user=request.user)
#     extra_form = ExtraProfileForm(instance=profile_obj, profile_obj=profile_obj, privacy_obj=privacy_obj)
#     profile_form = EditProfileForm(instance=request.user)
#
#     context = {
#         'extra_form': extra_form,
#         'profile_form': profile_form,
#     }
#
#     return render(request, 'users/test1.html', context)


@login_required
def send_friend_request(request, id):
    #if request.user.is_authenticated():
    user = get_object_or_404(User, id=id)
    frequest, created = FriendRequest.objects.get_or_create(
        from_user=request.user,
        to_user=user)
    return redirect('users:selected_user', id)


@login_required
def cancel_friend_request(request, id):
    #if request.user.is_authenticated():
    user = get_object_or_404(User, id=id)
    frequest = FriendRequest.objects.filter(
        from_user=request.user,
        to_user=user).first()
    frequest.delete()
    return redirect('users:selected_user', id)


@login_required
def accept_friend_request(request, id):
    from_user = get_object_or_404(User, id=id)
    frequest = FriendRequest.objects.filter(from_user=from_user, to_user=request.user).first()
    user1 = frequest.to_user
    user2 = from_user
    user1.profile.friends.add(user2.profile)
    user2.profile.friends.add(user1.profile)
    frequest.delete()
    return HttpResponseRedirect('/user/profile/')


@login_required
def delete_friend_request(request, id):
    from_user = get_object_or_404(User, id=id)
    frequest = FriendRequest.objects.filter(from_user=from_user, to_user=request.user).first()
    frequest.delete()
    return HttpResponseRedirect('/user/profile/')


@login_required
def list_of_friends(request, user_id):
    user_obj = get_object_or_404(User, id=user_id)
    profile_obj = Profile.objects.get(user=user_obj)
    friends_list = profile_obj.friends.all()
    paginator = Paginator(friends_list, 10)  # Show 10 contacts per page
    page = request.GET.get('page')
    paginator_friends_list = paginator.get_page(page)
    context = {'user': user_obj,
               'friends_list': paginator_friends_list}
    return render(request, 'users/list_of_friends.html', context)


def web_rules(request):
    context = {
     'rules_text': Rules.objects.get(id=1)
    }
    return render(request, 'Rules.html', context)


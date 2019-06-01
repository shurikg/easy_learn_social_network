from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import UserRegisterForm, NewUserProfileForm, NewUserDegreeForm, NewUserCourseForm, ProfileForm
from formtools.wizard.views import SessionWizardView
from .models import Profile, Privacy, FriendRequest, Rules, UserCourses, UserDegrees
from django.urls import reverse
from django.contrib.auth import authenticate, update_session_auth_hash, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.db.models import Q
import os
from EasyLearn.settings import MEDIA_ROOT
from .forms import (
    EditProfileForm,
    PasswordAuthenticationForm,
    EditPersonalInfoForm,
    EditMoreInfoForm,
    ExtraProfileForm,
    EditPrivacyForm,
    EditUserDegreeForm,
    EditUserCourseForm
)
from django.core.paginator import Paginator

User = get_user_model()


TEMP_PICTURES_FOLDER = 'temp_pictures'


class RegisterFormWizard(SessionWizardView):
    template_name = "users/register_wizard.html"
    form_list = [UserRegisterForm, NewUserProfileForm, NewUserDegreeForm, NewUserCourseForm]
    file_storage = FileSystemStorage(location=os.path.join(MEDIA_ROOT, TEMP_PICTURES_FOLDER))

    def get(self, request, *args, **kwargs):
        if not request.user.is_anonymous:
            messages.warning(request, f'You already signed in!')
            return home_page(request)
        return super(RegisterFormWizard, self).get(request, *args, **kwargs)

    def done(self, form_list, **kwargs):
        forms_dict = {}
        for form in form_list:
            forms_dict[type(form)] = form

        user_saved = False
        profile_saved = False
        degree_saved = False
        courses_saved = False
        privacy_saved = False

        try:
            user = forms_dict[UserRegisterForm].save(commit=False)
            user.username = str(user.username).lower()
            user.save()
            user_saved = True

            profile = forms_dict[NewUserProfileForm].save(commit=False)
            profile.user = user
            profile.save()
            profile_saved = True

            user_degree = forms_dict[NewUserDegreeForm].save(commit=False)
            user_degree.user_id = profile
            form_degree = forms_dict[NewUserDegreeForm].cleaned_data.get('degree')
            user_degree.degree_id = form_degree
            user_degree.save()
            degree_saved = True

            user_course = forms_dict[NewUserCourseForm].save(commit=False)
            user_course.user_id = profile
            form_courses = forms_dict[NewUserCourseForm].cleaned_data.get('course')
            user_course.save()
            user_course.course_id.set(form_courses)
            forms_dict[NewUserCourseForm].save_m2m()
            courses_saved = True
            privacy = Privacy()
            privacy.user = user
            privacy.save()
            privacy_saved = True

            messages.success(self.request, f'Registration successful!')
            return redirect(reverse('home'))
        except Exception as e:
            print(e)
            if privacy_saved:
                privacy.delete()
            if courses_saved:
                user_course.delete()
            if degree_saved:
                user_degree.delete()
            if profile_saved:
                profile.delete()
            if user_saved:
                user.delete()
            messages.error(self.request, e)
            return home_page(self.request)


def home_page(request):
    return render(request, 'users/home.html')


@login_required
def view_profile(request):
    user_obj = request.user
    profile_obj = Profile.objects.get(user=user_obj)
    user_courses = ()
    try:
        user_courses = tuple(course.course_name for course in tuple([c.course_id.all() for c in
                                                                     UserCourses.objects.filter(user_id=profile_obj)][
                                                                        0]))
    except IndexError as e:
        print(e)
    str_of_courses = ''
    for c in user_courses:
        str_of_courses += '{0}, '.format(str(c))
    if len(str_of_courses) > 0:
        str_of_courses = str_of_courses[:-2]
    user_degree = UserDegrees.objects.get(user_id=profile_obj)
    friend_requests_obj = FriendRequest.objects.filter(to_user=request.user)
    args = {'user': user_obj,
            'profile': profile_obj,
            'friend_requests': friend_requests_obj,
            'user_degree': user_degree,
            'user_courses': str_of_courses

            }
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
        form = EditMoreInfoForm(request.POST,request.FILES, instance=profile_obj)

        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('users:view_profile')
        else:
            messages.error(request, f'Invalid fields, your account has not been updated!')
            messages.error(request, form.errors)

    else:
        form = EditMoreInfoForm(instance=profile_obj)
    context = {
        'form': form,
    }
    return render(request, 'users/edit_more_info.html', context)


@login_required
def edit_educational_info(request):
    profile_obj = Profile.objects.get(user=request.user)
    user_course = UserCourses.objects.get(user_id=profile_obj)
    user_degree = UserDegrees.objects.get(user_id=profile_obj)
    if request.method == 'POST':
        courseForm = EditUserCourseForm(data=request.POST, instance=user_course)
        degreeForm = EditUserDegreeForm(data=request.POST, instance=user_degree)
        if courseForm.is_valid() and degreeForm.is_valid():
            degree = degreeForm.cleaned_data.get('degree')
            user_degree.degree_id = degree
            user_degree.save()

            courses = tuple(courseForm.cleaned_data.get('course'))
            UserCourses.objects.get(user_id=profile_obj).delete()
            new_courses = UserCourses(user_id=profile_obj)
            new_courses.save()
            for c in courses:
                new_courses.course_id.add(c)
            new_courses.save()
            # courseForm.save()
            # degreeForm.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('users:view_profile')
        else:
            messages.error(request, f'Invalid fields, your account has not been updated!')
            messages.error(request, courseForm.errors)
            messages.error(request, degreeForm.errors)
    else:
        courseForm = EditUserCourseForm(instance=user_course)
        degreeForm = EditUserDegreeForm(instance=user_degree)
    context = {
        'c_form': courseForm, 'd_form': degreeForm
    }
    return render(request, 'users/edit_educational_info.html', context)


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


@login_required
def show_selected_user(request, id):
    try:
        if request.user.id == int(id):
            return view_profile(request)
    except ValueError as e:
        print(e)

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
        'button_status': friend_status,
        'profile': profile_obj
    }
    return render(request, 'users/show_selected_user.html', context)


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


@login_required
def send_friend_request(request, id):
    user = get_object_or_404(User, id=id)
    frequest, created = FriendRequest.objects.get_or_create(
        from_user=request.user,
        to_user=user)
    return redirect('users:selected_user', id)


@login_required
def cancel_friend_request(request, id):
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


@login_required
def delete_friend(request, user_id):
    user = get_object_or_404(User, id=user_id)
    Profile.objects.get(user=user).friends.remove(
         Profile.objects.get(user=request.user))

    Profile.objects.get(user=request.user).friends.remove(
        Profile.objects.get(user=user))

    return show_selected_user(request, user_id)


def web_rules(request):
    context = {
     'rules_text': Rules.objects.all()
    }
    return render(request, 'Rules.html', context)

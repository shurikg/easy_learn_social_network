from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from files.forms import CreateNewFileForm, FilterFilesForm
import os
from EasyLearn.settings import MEDIA_ROOT
from files.models import File


@login_required
def show_files(request):
    files = File.objects.all()
    form = FilterFilesForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            category_filter = form.cleaned_data.get('category')
            degree_filter = form.cleaned_data.get('degree')
            user_filter = form.cleaned_data.get('user')
            if category_filter:
                if degree_filter:
                    if user_filter:
                        files = File.objects.filter(category=category_filter, related_degrees=degree_filter, owner=user_filter)
                    else:
                        files = File.objects.filter(category=category_filter, related_degrees=degree_filter)
                elif user_filter:
                    files = File.objects.filter(category=category_filter, owner=user_filter)
                else:
                    files = File.objects.filter(category=category_filter)
            elif degree_filter:
                if user_filter:
                    files = File.objects.filter(related_degrees=degree_filter, owner=user_filter)
                else:
                    files = File.objects.filter(related_degrees=degree_filter)
            elif user_filter:
                files = File.objects.filter(owner=user_filter)
            else:
                files = File.objects.all()

    args = {'files': files, 'form': form}
    return render(request, 'files/show_files.html', args)


@login_required
def add_new_file(request):
    if request.method == 'POST':
        form = CreateNewFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save(commit=False)
            file.owner = request.user
            file.save()
            form.save_m2m()
            return redirect('files:show_files')
    else:
        form = CreateNewFileForm
    return render(request, 'files/new_file.html', {"form": form})


@login_required
def download_file(request, file_id):
    file = File.objects.get(id=file_id)
    args = {'file': file, }
    return render(request, 'files/download_file.html', args)


@login_required
def delete_files(request):
    list_of_files = File.objects.filter(owner=request.user)
    if len(list_of_files) == 0:
        list_of_files = None
    return render(request, 'files/delete_files.html', {'files': list_of_files})


@login_required
def delete_one_file(request, file_id):
    try:
        file = File.objects.get(id=file_id)
        file_path = '{0}/{1}'.format(MEDIA_ROOT, file.file_url)
        os.remove(file_path)
        file.delete()
    except (FileNotFoundError, File.DoesNotExist) as e:
        print(e)
    return delete_files(request)

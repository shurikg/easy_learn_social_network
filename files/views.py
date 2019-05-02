from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from files.forms import CreateNewFileForm, filterFilesForm

# Create your views here.
from files.models import File
from users.views import User


@login_required
def show_files(request):
    files = File.objects.all()
    form = filterFilesForm(request.POST)
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
            return redirect('files:add_file')
    else:
        form = CreateNewFileForm
    return render(request, 'files/new_file.html', {"form": form})


def download_file(request, file_id):
    file = File.objects.get(id=file_id)
    args = {'file': file, }
    return render(request, 'files/download_file.html', args)


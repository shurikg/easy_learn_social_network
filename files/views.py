from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from files.forms import CreateNewFile, categoryForm

# Create your views here.
from files.models import File
from users.views import User


@login_required
def show_files(request):
    files = File.objects.all()
    form = categoryForm(request.POST)
    args = {'files1': files, 'form': form}
    return render(request, 'files/show_files.html', args)


@login_required
def add_new_file(request):
    if request.method == 'POST':
        form = CreateNewFile(request.POST, request.FILES)
        if form.is_valid():
            file = form.save(commit=False)
            file.owner = request.user
            file.save()
            return redirect('files:add_file')
    else:
        form = CreateNewFile
    return render(request, 'files/new_file.html', {"form": form})


def download_file(request, file_id):
    file = File.objects.get(id=file_id)
    args = {'file': file, }
    return render(request, 'files/download_file.html', args)


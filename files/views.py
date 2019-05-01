from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from files.forms import CreateNewFile

# Create your views here.
from files.models import File
from users.views import User


@login_required
def show_files(request):
    query = request.GET.get('q')
    if query:
        users = User.objects.filter(Q(first_name=query) | Q(last_name=query))
    else:
        users = User.objects.all().order_by('last_name')
    args = {'users': users}
    return render(request, 'files/show_files.html', args)


@login_required
def add_new_file(request):
    form = CreateNewFile
    return render(request, 'files/new_file.html', {"form": form})


def download_file(request, file_id):
    file = File.objects.get(id=file_id)
    args = {'file': file, }
    return render(request, 'files/download_file.html', args)


from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from files.forms import SelectCategoryForm
from files.models import File
from users.views import User


@login_required
def show_files(request):
    form = SelectCategoryForm(request.POST)
    if request.method == 'POST':
        category = form.cleaned_data.get('category')
        files = File.objects.filter(category=category)
    else:
        files = File.objects.all()

    args = {'files': files, 'form': form}
    return render(request, 'files/show_files.html', args)

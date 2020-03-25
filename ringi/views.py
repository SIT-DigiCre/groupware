from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Ringi, Status
from .forms import RingiForm

@login_required(login_url='/admin/login/')
def index(request, page=1):
    # GETアクセス時の処理
    display_num = 10 # 1ページに表示するレコードの件数
    ringis = Ringi.objects.all()
    ringis_page = Paginator(ringis, display_num)
    statuses = Status.objects.all()

    params = {
       'ringis': ringis_page.get_page(page),
       'statuses': statuses,
    }
    return render(request, 'ringi/index.htm', params)

@login_required(login_url='/admin/login/')
def create(request):
    params = {
        'form': RingiForm()
    }
    # POSTアクセス時の処理
    if request.method == 'POST':
        obj = Ringi()
        obj.owner = request.user
        obj.status = Status.objects.all().first()
        ringi = RingiForm(request.POST, instance=obj)
        ringi.save()
        return redirect(to='/ringi')

    # GETアクセス時の処理
    return render(request, 'ringi/create.htm', params)

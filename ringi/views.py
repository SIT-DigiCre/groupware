from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator
from django.db.models import Count
from .models import Ringi, Status
from .forms import RingiForm, RingiEditForm

@login_required()
def index(request):
    # GETアクセス時の処理
    display_num = 10 # 1ページに表示するレコードの件数
    
    if 'status' in request.GET:
        ringis = Ringi.objects.filter(status=request.GET['status'])
    else:
        ringis = Ringi.objects.all()
    
    ringis_page = Paginator(ringis, display_num)
    page = request.GET.get('page')

    params = {
        'title': '費用申請',
        'page_obj': ringis_page.get_page(page),
        'uncompleted_statuses': Status.objects.filter(is_completed=False),
        'records_num': ringis.count(),
    }
    return render(request, 'ringi/index.htm', params)

@login_required()
def create(request):
    params = {
        'title': '新規',
        'form': RingiForm()
    }
    # POSTアクセス時の処理
    if request.method == 'POST':
        obj = Ringi()
        obj.owner = request.user
        obj.status = Status.objects.all().first()
        ringi = RingiForm(request.POST,request.FILES, instance=obj)
        ringi.save()
        return redirect(to='/ringi')

    # GETアクセス時の処理
    return render(request, 'ringi/create.htm', params)

@login_required()
def show(request, id):
    params = {
        'title': '詳細',
        'ringi': Ringi.objects.get(id=id)
    }
    return render(request, 'ringi/show.htm', params)

@login_required()
@permission_required('ringi.change_ringi')
def edit(request, id):
    obj = Ringi.objects.get(id=id)
    # POSTアクセス時の処理
    if request.method == 'POST':
        ringi = RingiEditForm(request.POST, instance=obj)
        ringi.save()
        return redirect(to="/ringi")
    
    # GETアクセス時の処理
    params = {
        'title': '編集',
        'id': obj.id,
        'form': RingiEditForm(instance=obj)
    }
    return render(request, 'ringi/edit.htm', params)

@login_required()
@permission_required('ringi.delete_ringi')
def delete(request, id):
    ringi = Ringi.objects.get(id=id)
    # POSTアクセス時の処理
    if request.method == 'POST':
        ringi.delete()
        return redirect(to="/ringi")

    # GETアクセス時の処理
    params = {
        'title': '削除',
        'ringi': ringi
    }
    return render(request, 'ringi/delete.htm', params)

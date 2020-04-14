from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import *
from .forms import ToolForm
# Create your views here.
@login_required(login_url='/admin/login/')
def index(request):
    # GETアクセス時の処理
    tools = Tool.objects.all()

    params = {
       'tools': tools,
    }
    return render(request, 'tool/index.htm', params)

@login_required(login_url='/admin/login/')
def show(request,id=-1):
    if id==-1:
        return redirect(to='/tool')
    tool = Tool.objects.filter(id=id).first()
    params={
        'tool':tool
    }
    return render(request,'tool/show.htm',params)


@login_required(login_url='/admin/login/')
def create(request):
    params = {
        'form': ToolForm()
    }
    # POSTアクセス時の処理
    if request.method == 'POST':
        obj = Tool()
        obj.editor = request.user
        tool = ToolForm(request.POST,request.FILES, instance=obj)
        tool.save()
        return redirect(to='/tool')

    # GETアクセス時の処理
    return render(request, 'tool/create.htm', params)
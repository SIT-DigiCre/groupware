from django.shortcuts import *
from django.contrib.auth.decorators import login_required

from tool.models import *
from .models import *
from .forms import *

@login_required(login_url='/admin/login/')
def index(request):
    # GETアクセス時の処理
    profiles = Profile.objects.all()
    params = {
        'profiles':profiles,
    }
    return render(request, 'member/index.htm', params)


@login_required(login_url='/admin/login/')
def show(request,id):
    # GETアクセス時の処理
    profile = Profile.objects.filter(id=id).first()
    params = {
        'profile':profile,
        'is_currentusers_data':request.user.id == profile.user.id,
    }
    return render(request, 'member/show.htm', params)

@login_required(login_url='/admin/login/')
def edit(request):
    profile = Profile.objects.filter(id=request.user.id).first()
    # POSTアクセス時（返信時）の処理
    if request.method == 'POST':
        if 'add-usertool-form' in request.POST:
            usertool_form = UserToolForm(request.POST)
            if usertool_form.is_valid():
                usertool = UserTool()
                usertool.level = usertool_form.cleaned_data['level']
                usertool.user=request.user
                usertool.tool = Tool.objects.filter(name__exact=usertool_form.cleaned_data['c_tool']).first()
                usertool.profile = profile
                usertool.save()
            

        
        # 同じページにリダイレクトするだけなので、もっと賢い書き方あるはず
        return redirect(to='/member/edit' )
    # GETアクセス時の処理
    params = {
        'add_usertool_form': UserToolForm()
    }
    return render(request, 'member/edit.htm', params)
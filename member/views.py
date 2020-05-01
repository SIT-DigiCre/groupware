from django.shortcuts import *
from django.contrib.auth.decorators import login_required

from tool.models import *
from .models import *
from .forms import *
from account.forms import UserEditForm

@login_required()
def index(request):
    # GETアクセス時の処理
    profiles = Profile.objects.all()
    params = {
        'profiles':profiles,
    }
    return render(request, 'member/index.htm', params)


@login_required()
def show(request,id):
    # GETアクセス時の処理
    profile = Profile.objects.filter(id=id).first()
    params = {
        'profile':profile,
        'is_currentusers_data':request.user.id == profile.user.id,
    }
    return render(request, 'member/show.htm', params)

@login_required()
def edit(request):
    profile = Profile.objects.filter(id=request.user.id).first()
    # POSTアクセス時（返信時）の処理
    if request.method == 'POST':
        if 'add-usertool-form' in request.POST:
            usertool_form = UserToolForm(request.POST)
            if usertool_form.is_valid():
                usertool = UserTool()
                usertool.level = usertool_form.cleaned_data['level']
                usertool.tool = usertool_form.cleaned_data['tool']
                usertool.profile = profile
                usertool.save()
        if 'user-edit-form' in request.POST:
            user_form = UserEditForm(request.POST,request.FILES,instance = request.user)
            user_form.save()
        if 'profile-edit-form' in request.POST:
            profile_form = ProfileForm(request.POST,request.FILES,instance = request.user.profile)
            profile = profile_form.save(commit=True)
        
        # 同じページにリダイレクトするだけなので、もっと賢い書き方あるはず
        return redirect(to='/member/edit' )
    # GETアクセス時の処理
    params = {
        'add_usertool_form': UserToolForm(),
        'user_form':UserEditForm(instance=request.user),
        'profile_form':ProfileForm(instance=request.user.profile)
    }
    return render(request, 'member/edit.htm', params)

@login_required()
def me(request):
    # GETアクセス時の処理
    profile = request.user.profile
    return redirect(to='/member/'+str(profile.id))
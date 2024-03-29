from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from tool.models import Tool
from .models import Division, Profile, UserTool
from .forms import UserToolForm, ProfileForm
from account.forms import UserEditForm

@login_required()
def index(request):
    # GETアクセス時の処理
    display_num = 30
    page = request.GET.get('page')
    
    if 'search_word' in request.GET:
        word = request.GET['search_word']
        profiles = Profile.objects.filter(user__username__contains=word)
    else:
        profiles = Profile.objects.all()

    num = profiles.count()
    profiles_page = Paginator(profiles, display_num)
    params = {
        'num': num,
        'page_obj': profiles_page.get_page(page),
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
    profile = Profile.objects.filter(user=request.user).first()
    # POSTアクセス時（返信時）の処理
    if request.method == 'POST':
        # ツールの編集
        if 'add-usertool-form' in request.POST:
            toolid = request.POST['toolchoice']
            tool = Tool.objects.filter(id=toolid).first()
            usertool = UserTool.objects.filter(tool=tool,profile=profile)
            if len(usertool.all()) == 0:
                usertool = UserTool()
            else:
                usertool = usertool.first()
            usertool.profile = profile
            usertool.tool = tool
            usertool.level = int(request.POST['toollevel'])
            usertool.save()

        # 班の編集
        if 'add-division-form' in request.POST:
            divisionid = int(request.POST['divisionchoice'])
            division = Division.objects.filter(id=divisionid).first()
            profile.divisions.add(division)

        # ユーザーデータ編集
        if 'user-edit-form' in request.POST:
            user_form = UserEditForm(request.POST,request.FILES,instance = request.user)
            user_form.save()
            profile_form = ProfileForm(request.POST,request.FILES,instance = request.user.profile)
            profile = profile_form.save(commit=True)
        
        # 自分のプロフィールにリダイレクト
        return redirect(to='/member/me')
    exist_tools = []
    for usertool in profile.usertool_set.all():
        exist_tools.append(usertool.tool)
    
    # GETアクセス時の処理
    params = {
        'add_usertool_form': UserToolForm(),
        'user_form':UserEditForm(instance=request.user),
        'profile_form':ProfileForm(instance=request.user.profile),
        'tools':Tool.objects.all(),
        'exist_tools':exist_tools,
        'divisions':Division.objects.all(),
        'profile':profile,
    }
    return render(request, 'member/edit.htm', params)

@login_required()
def me(request):
    # GETアクセス時の処理
    profile = request.user.profile
    return redirect(to='/member/'+str(profile.id))
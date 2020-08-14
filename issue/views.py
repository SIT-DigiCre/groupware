from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator
from django.db.models import Count
from .models import Status, Issue
from .forms import IssueForm, IssueEditForm

@login_required()
def index(request, page=1):
    # GETアクセス時の処理
    display_num = 10 # 1ページに表示するレコードの件数
    
    if 'status' in request.GET:
        issues = Issue.objects.filter(status=request.GET['status'])
    else:
        issues = Issue.objects.all()
    
    issues_page = Paginator(issues, display_num)

    params = {
        'title': 'バグ報告・機能改善',
        'issues': issues_page.get_page(page),
        'uncompleted_statuses': Status.objects.filter(is_completed=False),
        'records_num': issues.count(),
    }
    return render(request, 'issue/index.htm', params)

@login_required()
def create(request):
    params = {
        'title': '新規',
        'form': IssueForm(),
    }
    # POSTアクセス時の処理
    if request.method == 'POST':
        obj = Issue()
        obj.user = request.user
        obj.status = Status.objects.all().first()
        issue = IssueForm(request.POST, instance=obj)
        if issue.is_valid():
            issue.save()
        else:
            # このエラー表示、ログに変えたほうがいいかもしれないです
            # 以下同じく
            print(issue.errors)
        return redirect(to='issue:index')

    # GETアクセス時の処理
    return render(request, 'issue/create.htm', params)

@login_required()
def show(request, id):
    params = {
        'title': '詳細',
        'issue': Issue.objects.get(id=id)
    }
    return render(request, 'issue/show.htm', params)

@login_required()
@permission_required('issue.change_issue')
def edit(request, id):
    obj = Issue.objects.get(id=id)
    # POSTアクセス時の処理
    if request.method == 'POST':
        issue = IssueEditForm(request.POST, instance=obj)
        if issue.is_valid():
            issue.save()
        else:
            print(issue.errors)
        return redirect(to='issue:index')
    
    # GETアクセス時の処理
    form = IssueEditForm(instance=obj)
    form.fields['assignee'].queryset = User.objects.filter(is_superuser=True)
    params = {
        'title': '編集',
        'id': obj.id,
        'form': form,
    }
    return render(request, 'issue/edit.htm', params)

@login_required()
@permission_required('issue.delete_issue')
def delete(request, id):
    issue = Issue.objects.get(id=id)
    # POSTアクセス時の処理
    if request.method == 'POST':
        issue.delete()
        return redirect(to='issue:index')

    # GETアクセス時の処理
    params = {
        'title': '削除',
        'issue': issue
    }
    return render(request, 'issue/delete.htm', params)

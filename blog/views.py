from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Article,ArticleTag
from .forms import *
# Create your views here.
def index(request,page=1):
    articles_data = Paginator(Article.objects.all(),10)
    params = {
        'articles':articles_data.get_page(page),
    }
    return render(request,'blog/index.htm',params)

def show(request,id=1):
    article = Article.objects.filter(id=id).first()
    params = {
        'article':article,
        'is_edit_user':request.user == article.member,
    }
    return render(request,'blog/show.htm',params)

@login_required(login_url='/admin/login/')
def edit(request,id=1):
    pass

@login_required(login_url='/admin/login/')
def create(request):
    if request.method=='POST':
        article = Article()
        article.member = request.user
        article_f = NewArticleForm(request.POST, instance=article)
        article_f.save()
        return redirect(to='/blog')
    params = {
        'form':NewArticleForm()
    }
    return render(request,'blog/create.htm',params)
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
        'is_login_user':request.user.is_authenticated,
    }
    return render(request,'blog/index.htm',params)

def show(request,id=1):
    article = Article.objects.filter(id=id).first()
    params = {
        'article':article,
        'is_edit_user':request.user == article.member,
        'is_login_user':request.user.is_authenticated,
    }
    return render(request,'blog/show.htm',params)

@login_required(login_url='/admin/login/')
def edit(request,id=1):
    article = Article.objects.filter(id=id).first()
    if request.method == 'POST' and request.user == article.member:
        article_form = EditArticleForm(request.POST,instance = article)
        article_post = article_form.save(commit=False)
        article_post.member=request.user
        article_post.save()
        return redirect(to='/blog/article/'+str(article_post.id))

    params = {
        'form':EditArticleForm(instance=article),
        'article':article,
        'is_login_user':request.user.is_authenticated,
    }
    return render(request,'blog/edit.htm',params)

@login_required(login_url='/admin/login/')
def create(request):
    if request.method=='POST':
        article = Article()
        article.member = request.user
        article_f = NewArticleForm(request.POST, instance=article)
        article_f.save()
        return redirect(to='/blog')
    params = {
        'form':NewArticleForm(),
        'is_login_user':request.user.is_authenticated,
    }
    return render(request,'blog/create.htm',params)
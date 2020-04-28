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

@login_required(login_url='/admin/login/')
def create_tag(request):
    if request.method=='POST':
        article_tag = ArticleTag()
        article_tag_f = NewArticleTagForm(request.POST, instance=article_tag)
        article_tag_f.save()
        return redirect(to='/blog')
    params = {
        'form':NewArticleTagForm(),
        'is_login_user':request.user.is_authenticated,
    }
    return render(request,'blog/tag_create.htm',params)

def show_tag(request,id=1):
    article_tag = ArticleTag.objects.filter(id=id).first()
    params = {
        'article_tag':article_tag,
        'is_login_user':request.user.is_authenticated,
    }
    return render(request,'blog/tag_show.htm',params)

@login_required(login_url='/admin/login/')
def edit_tag(request,id=1):
    article_tag = ArticleTag.objects.filter(id=id).first()
    if request.method == 'POST':
        article_tag_form = EditArticleTagForm(request.POST,instance = article_tag)
        article_tag_post = article_tag_form.save(commit=False)
        article_tag_post.member=request.user
        article_tag_post.save()
        return redirect(to='/blog/tag/'+str(article_tag_post.id))

    params = {
        'form':EditArticleTagForm(instance=article_tag),
        'article_tag':article_tag,
        'is_login_user':request.user.is_authenticated,
    }
    return render(request,'blog/tag_edit.htm',params)

def index_tag(request):
    params = {
        'is_login_user':request.user.is_authenticated,
        'article_tags':ArticleTag.objects.all(),
        
    }
    return render(request,'blog/tag_index.htm',params)

def edit_art_tags(request,id=1):
    article = Article.objects.filter(id=id).first()
    if request.method=='POST' and request.user == article.member:
        choice_id = request.POST['tagchoice']
        print('choice_str:'+choice_id)
        article_tag = ArticleTag.objects.filter(id=choice_id).first()
        article.article_tags.add(article_tag)
        article.save()

        return redirect(to='/blog/article/'+str(article.id)+'/tags')

    params = {
        'article_tags':ArticleTag.objects.all(),
        'article':article,
        'is_edit_user':request.user == article.member,
        'is_login_user':request.user.is_authenticated,
    }
    return render(request,'blog/article_tag_edit.htm',params)

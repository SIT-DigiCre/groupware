from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils import timezone

import datetime

from .models import Article, ArticleTag, BlogEvent, EventArticle
from .forms import NewArticleForm, EditArticleForm, NewArticleTagForm, EditArticleTagForm,EventArticleForm
# Create your views here.
def index(request):
    print('hoge')
    display_num = 30
    page = request.GET.get('page')

    articles_data = Paginator(Article.objects.filter(is_active=True), display_num)
    params = {
        'page_obj': articles_data.get_page(page),
        'is_login_user': request.user.is_authenticated,
    }
    return render(request, 'blog/index.htm', params)

def show(request,id=1):
    article = Article.objects.filter(id=id).first()
    if article.is_active is False and article.member != request.user:
        return redirect(to='/blog')
    params = {
        'article':article,
        'is_edit_user':request.user == article.member,
        'is_login_user':request.user.is_authenticated,
    }
    return render(request,'blog/show.htm',params)

@login_required()
def edit(request,id=1):
    article = Article.objects.filter(id=id).first()
    if request.method == 'POST' and request.user == article.member:
        if 'save-pub-btn' in request.POST and article.is_active is False:
            article.pub_date = timezone.now()
            article.is_active = True
        elif 'save-nopub-btn' in request.POST:
            article.is_active = False
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

@login_required()
def create(request):
    if request.method=='POST':
        article = Article()
        article.member = request.user
        article.is_active = False
        if 'save-pub-btn' in request.POST:
            article.pub_date = timezone.now()
            article.is_active = True
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
    articles = Article.objects.filter(article_tags=article_tag).filter(is_active=True)
    params = {
        'articles': articles,
        'tag': article_tag,
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

def delete_art_tag(request,art_id,tag_id):
    article = Article.objects.filter(id=art_id).first()
    tag = ArticleTag.objects.filter(id=tag_id).first()
    article.article_tags.remove(tag)
    return redirect(to='/blog/article/'+str(article.id)+'/tags')

def relay(request, id):
    blogEvent = BlogEvent.objects.get(id=id)
    month = blogEvent.month
    year = blogEvent.year
    
    # カレンダー（動的に生成したい）
    calender = [
        [
            [0, 3, 4, 5, 6, 7, 8],
            [9, 10, 11, 12, 13, 14, 15],
            [16, 17, 18, 19, 20, 21, 22],
            [23, 24, 25, 26, 27, 28, 29],
            [30, 31, 0, 0, 0, 0, 0],
        ],
        [
            [0, 0, 1, 2, 3, 4, 5],
            [6, 7, 8, 9, 10, 11, 12],
            [13, 14, 15, 16, 17, 18, 19],
            [20, 21, 22, 23, 24, 25, 0]
        ]
    ]

    # その日がすでに登録されているかどうか
    is_registerd = [False for s in range(32)]

    for day in range(1, 32):
        dt = datetime.datetime(year, month, day)
        ea = EventArticle.objects.filter(event__id=id, release_date=dt)
        if ea.exists():
            is_registerd[day] = ea.first()
        else:
            is_registerd[day] = False
        
        print(str(day) + ": " + str(is_registerd[day]))


    params = {
        'id': id,
        'year': year,
        'month': month,
        'calender': calender[id-1],
        'is_registerd': is_registerd,
        'event_article': EventArticle.objects.filter(event__id=id),
        'event': blogEvent,
    }
    return render(request, 'blog/relay.htm', params)

@login_required()
def relay_add_check(request, id, year, month, day):
    today = datetime.datetime(year, month, day)
    form = EventArticleForm()
    form.fields['article'].queryset = Article.objects.filter(member=request.user)

    params = {
        'id': id,
        'year': year,
        'month': month,
        'day': day,
        'date': today,
        'form': form,
    }
    return render(request, 'blog/relay_add_check.htm', params)

@login_required()
def relay_add(request, id, year, month, day):
    if request.method=='POST':
        dt = datetime.datetime(year, month, day)

        # すでに登録されていたら
        if EventArticle.objects.filter(event__id=id, release_date=dt).exists():
            return HttpResponse("すでに他の人に登録されています")

        ea = EventArticle()
        ea.event = BlogEvent.objects.get(id=id)
        ea.release_date = dt
        ea.user = request.user

        form = EventArticleForm(request.POST, instance=ea)
        ea_f = form.save(commit=False)
        ea_f.save()

    return redirect(to='blog.relay', id=id)

@login_required()
def relay_edit(request, id, year, month, day):
    dt = datetime.datetime(year, month, day)
    obj = EventArticle.objects.filter(event__id=id, release_date=dt).first()
    form = EventArticleForm(instance=obj)
    form.fields['article'].queryset = Article.objects.filter(member=request.user)

    if request.method=='POST':
        form = EventArticleForm(request.POST, instance=obj)
        form.save()
        return redirect(to='blog.relay', id=id)

    params = {
        'id': id,
        'year': year,
        'month': month,
        'day': day,
        'form': form
    }
    return render(request,'blog/relay_edit.htm',params)

@login_required()
def relay_delete(request, id, year, month, day):
    dt = datetime.datetime(year, month, day)
    obj = EventArticle.objects.filter(event__id=id, release_date=dt).first()
    obj.delete()

    return redirect(to='blog.relay', id=id)


def event_index(request,event_name):
    #ここにイベント一覧ページを用意する
    pass

@login_required(login_url='/admin/login/')
def mypage(request):
    articles = Article.objects.filter(member=request.user)
    articles_pub = articles.filter(is_active=True)
    articles_nopub = articles.filter(is_active=False)
    params = {
        'articles_pub':articles_pub,
        'articles_nopub':articles_nopub,
        'is_login_user':request.user.is_authenticated,
    }
    return render(request,'blog/mypage.htm',params)

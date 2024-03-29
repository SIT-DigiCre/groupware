from os import stat
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, FileResponse, response
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils import timezone
from rest_framework import viewsets, pagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly

import datetime

# Image draw
import io
from PIL import Image, ImageDraw, ImageFont
from typing import List
from enum import Enum

from .models import Article, ArticleTag, BlogEvent, EventArticle
from .forms import NewArticleForm, EditArticleForm, NewArticleTagForm, EditArticleTagForm, EventArticleForm
from .serializer import ArticleSerializer, ArticleTagSerializer
# Create your views here.


def index(request):
    display_num = 30
    page = request.GET.get('page')

    articles_data = Paginator(
        Article.objects.filter(is_active=True), display_num)
    params = {
        'page_obj': articles_data.get_page(page),
        'is_login_user': request.user.is_authenticated,
    }
    return render(request, 'blog/index.htm', params)


def show(request, id=1):
    article = Article.objects.filter(id=id).first()
    if article.is_active is False and article.member != request.user:
        return redirect(to='/blog')
    params = {
        'article': article,
        'is_edit_user': request.user == article.member,
        'is_login_user': request.user.is_authenticated,
    }
    return render(request, 'blog/show.htm', params)


@login_required()
def edit(request, id=1):
    article = Article.objects.filter(id=id).first()
    if request.method == 'POST' and request.user == article.member:
        if 'save-pub-btn' in request.POST and article.is_active is False:
            article.pub_date = timezone.now()
            article.is_active = True
        elif 'save-nopub-btn' in request.POST:
            article.is_active = False
        article_form = EditArticleForm(request.POST, instance=article)
        article_post = article_form.save(commit=False)
        article_post.member = request.user
        article_post.save()
        return redirect(to='/blog/article/'+str(article_post.id))

    params = {
        'form': EditArticleForm(instance=article),
        'article': article,
        'is_login_user': request.user.is_authenticated,
    }
    return render(request, 'blog/edit.htm', params)


@login_required()
def create(request):
    if request.method == 'POST':
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
        'form': NewArticleForm(),
        'is_login_user': request.user.is_authenticated,
    }
    return render(request, 'blog/create.htm', params)


@login_required(login_url='/admin/login/')
def create_tag(request):
    if request.method == 'POST':
        article_tag = ArticleTag()
        article_tag_f = NewArticleTagForm(request.POST, instance=article_tag)
        article_tag_f.save()
        return redirect(to='/blog')
    params = {
        'form': NewArticleTagForm(),
        'is_login_user': request.user.is_authenticated,
    }
    return render(request, 'blog/tag_create.htm', params)


def show_tag(request, id=1):
    article_tag = ArticleTag.objects.filter(id=id).first()
    articles = Article.objects.filter(
        article_tags=article_tag).filter(is_active=True)
    params = {
        'articles': articles,
        'tag': article_tag,
        'is_login_user': request.user.is_authenticated,
    }
    return render(request, 'blog/tag_show.htm', params)


@login_required(login_url='/admin/login/')
def edit_tag(request, id=1):
    article_tag = ArticleTag.objects.filter(id=id).first()
    if request.method == 'POST':
        article_tag_form = EditArticleTagForm(
            request.POST, instance=article_tag)
        article_tag_post = article_tag_form.save(commit=False)
        article_tag_post.member = request.user
        article_tag_post.save()
        return redirect(to='/blog/tag/'+str(article_tag_post.id))

    params = {
        'form': EditArticleTagForm(instance=article_tag),
        'article_tag': article_tag,
        'is_login_user': request.user.is_authenticated,
    }
    return render(request, 'blog/tag_edit.htm', params)


def index_tag(request):
    params = {
        'is_login_user': request.user.is_authenticated,
        'article_tags': ArticleTag.objects.all(),

    }
    return render(request, 'blog/tag_index.htm', params)


def edit_art_tags(request, id=1):
    article = Article.objects.filter(id=id).first()
    if request.method == 'POST' and request.user == article.member:
        choice_id = request.POST['tagchoice']
        print('choice_str:'+choice_id)
        article_tag = ArticleTag.objects.filter(id=choice_id).first()
        article.article_tags.add(article_tag)
        article.save()

        return redirect(to='/blog/article/'+str(article.id)+'/tags')

    params = {
        'article_tags': ArticleTag.objects.all(),
        'article': article,
        'is_edit_user': request.user == article.member,
        'is_login_user': request.user.is_authenticated,
    }
    return render(request, 'blog/article_tag_edit.htm', params)


def delete_art_tag(request, art_id, tag_id):
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
    form.fields['article'].queryset = Article.objects.filter(
        member=request.user)

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
    if request.method == 'POST':
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
    form.fields['article'].queryset = Article.objects.filter(
        member=request.user)

    if request.method == 'POST':
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
    return render(request, 'blog/relay_edit.htm', params)


@login_required()
def relay_delete(request, id, year, month, day):
    dt = datetime.datetime(year, month, day)
    obj = EventArticle.objects.filter(event__id=id, release_date=dt).first()
    obj.delete()

    return redirect(to='blog.relay', id=id)


def event_index(request, event_name):
    # ここにイベント一覧ページを用意する
    pass


@login_required(login_url='/admin/login/')
def mypage(request):
    articles = Article.objects.filter(member=request.user)
    articles_pub = articles.filter(is_active=True)
    articles_nopub = articles.filter(is_active=False)
    params = {
        'articles_pub': articles_pub,
        'articles_nopub': articles_nopub,
        'is_login_user': request.user.is_authenticated,
    }
    return render(request, 'blog/mypage.htm', params)


class TextAlign(Enum):
    Left = 1
    Center = 2
    Right = 3


def wrap_text(img, text: str, font, max_width: int) -> List[str]:
    draw = ImageDraw.Draw(img)
    text_list = [text]
    while max_width < draw.textsize(text_list[-1], font=font)[0]:
        test_text = text_list[-1]
        while max_width < draw.textsize(test_text, font=font)[0]:
            test_text = test_text[:-1]
        text_list.append(text_list[-1][len(test_text):])
        text_list[-2] = test_text
    return text_list


def add_text_to_image(img, x: int, y: int, width: int, lines: int, text: str, font_size, font_color, text_align: TextAlign):
    font = ImageFont.truetype("blog/font.ttf", font_size)
    draw = ImageDraw.Draw(img)
    wrapped_text = wrap_text(img, text, font, width)
    if lines < len(wrapped_text):
        wrapped_text = wrapped_text[:lines]
        wrapped_text[-1] += '…'
    w, h = img.size
    for i, t in enumerate(wrapped_text):
        if text_align == TextAlign.Center:
            position = (x + width / 2 - draw.textsize(t, font=font)
                        [0] / 2, y + i * font_size)
        elif text_align == TextAlign.Right:
            position = (x + width - draw.textsize(t, font=font)
                        [0], y + i * font_size)
        else:
            position = (x, y + i * font_size)
        draw.text(position, t, font_color, font=font)
    return img


class GenOGPImageAPIView(APIView):
    def get(self, request, id):
        img = Image.open('blog/blog_ogp.png')
        article = Article.objects.filter(id=id)
        if len(article) == 0:
            title = 'Not Found'
            member_username = ''
        else:
            title = article[0].title
            member = article[0].member
            member_username = member.username
            # member_icon = mamber.icon

        textbox_width = 800
        img_w, img_h = img.size
        img = add_text_to_image(
            img,
            (img_w - textbox_width) / 2,
            200,
            textbox_width,
            4,
            title,
            70,
            (0, 0, 0),
            TextAlign.Left
        )
        img = add_text_to_image(
            img,
            (img_w - textbox_width) / 2,
            500,
            textbox_width,
            2,
            member_username,
            50,
            (0, 0, 0),
            TextAlign.Right
        )
        file_obj = io.BytesIO()
        img.save(file_obj, 'PNG')
        file_obj.seek(0)
        fr = FileResponse(file_obj)
        fr['Content-Type'] = 'image/PNG'
        return fr


# REST_APIs

class ArticleResultsPagination(pagination.PageNumberPagination):
    page_size = 15


class ArticleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Article.objects.order_by('-pub_date').filter(is_active=True)
    serializer_class = ArticleSerializer
    pagination_class = ArticleResultsPagination
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.view_count += 1
        instance.save()
        serializer = ArticleSerializer(instance=instance)
        return Response(serializer.data)


class MyArticlesViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    pagination_class = ArticleResultsPagination

    def get_queryset(self):
        return Article.objects.filter(member=self.request.user).order_by('-pub_date')

    def perform_create(self, serializer):
        if serializer.validated_data['is_active']:
            return serializer.save(member=self.request.user,pub_date=timezone.datetime.now())
        return serializer.save(member=self.request.user)

    def perform_update(self, serializer):
        current_article = get_object_or_404(Article, id=serializer.validated_data['id'])
        if serializer.validated_data['is_active'] and not current_article.is_active:
            return serializer.save(member=self.request.user,pub_date=timezone.datetime.now())
        return serializer.save(member=self.request.user)


class ArticleTagViewSet(viewsets.ModelViewSet):
    queryset = ArticleTag.objects.all()
    serializer_class = ArticleTagSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

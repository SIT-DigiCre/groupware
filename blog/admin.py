from django.contrib import admin
from .models import Article, ArticleTag, BlogEvent, EventArticle
# Register your models here.
admin.site.register(Article)
admin.site.register(ArticleTag)
admin.site.register(BlogEvent)
admin.site.register(EventArticle)

from rest_framework import serializers
from .models import Article, ArticleTag


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('id', 'member', 'title', 'content', 'article_image', 'article_tags', 'is_active',  'pub_date')


class ArticleTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleTag
        fields = ('id', 'name', 'content', 'pub_date')

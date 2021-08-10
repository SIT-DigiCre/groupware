from rest_framework import serializers
from .models import Article,ArticleTag


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('id','member','title','content','pub_date','pub_date')

class ArticleTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleTag
        fields = ('id','name','content','pub_date')
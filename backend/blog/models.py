from django.db import models
from account.models import User
from work.models import Work
# マークダウン使用のため
from markdownx.utils import markdownify

from mdeditor.fields import MDTextField

class ArticleTag(models.Model):
    name = models.CharField(max_length=30)
    content = MDTextField('Contents')
    pub_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
    def formatted_markdown(self):
        return markdownify(self.content) # モデルデータをMarkDown形式に変換してくれる


class Article(models.Model):
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = MDTextField('Contents', blank=True)
    article_image = models.URLField(verbose_name='サムネイル画像URL', blank=True)
    article_tags = models.ManyToManyField(ArticleTag,blank=True)
    relates_works=models.ManyToManyField(Work,blank=True)
    pub_date = models.DateTimeField(blank=True,null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-pub_date',) # 新着順にする

    def __str__(self):
        return self.title

    def formatted_markdown(self):
        return markdownify(self.content) # モデルデータをMarkDown形式に変換してくれる
    
    


# ブログリレーなどのイベント
class BlogEvent(models.Model):
    name = models.CharField(max_length=100)
    content = MDTextField('Contents', default='')
    year = models.IntegerField(default=2020)
    month = models.IntegerField(default=8)

    def __str__(self):
        return self.name

    def formatted_markdown(self):
        return markdownify(self.content) # モデルデータをMarkDown形式に変換してくれる


class EventArticle(models.Model):
    event = models.ForeignKey(BlogEvent, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True)
    release_date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ('release_date',) # 日付順

    def __str__(self):
        return str(self.release_date)

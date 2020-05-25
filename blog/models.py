from django.db import models
from account.models import User
from tool.models import Tool
from work.models import Work
# マークダウン使用のため
from markdownx.models import MarkdownxField
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
    content = MDTextField('Contents')
    article_image = models.ImageField(upload_to='article_image/', default='null')
    article_tags = models.ManyToManyField(ArticleTag,blank=True)
    relates_works=models.ManyToManyField(Work,blank=True)
    pub_date = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ('-pub_date',) # 新着順にする

    def __str__(self):
        return self.title

    def formatted_markdown(self):
        return markdownify(self.content) # モデルデータをMarkDown形式に変換してくれる



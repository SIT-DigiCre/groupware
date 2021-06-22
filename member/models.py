from django.db import models
from account.models import User
from tool.models import Tool
# マークダウン使用のため
from markdownx.utils import markdownify
from mdeditor.fields import MDTextField

class Division(models.Model):
    name = models.CharField(max_length = 20) #PGなど班の情報
    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    generation = models.IntegerField(blank=True)
    message = models.CharField(verbose_name='ひとこと', max_length = 140)
    intro = MDTextField('自己紹介',blank=True)
    divisions = models.ManyToManyField(Division)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    def formatted_markdown(self):
        return markdownify(self.intro) # モデルデータをMarkDown形式に変換してくれる

class UserTool(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE)
    level = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tool.name

from django.db import models
from account.models import User
from tool.models import Tool
from django.db.models.signals import post_save
from django.dispatch import receiver
# マークダウン使用のため
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify

# Create your models here.
class Division(models.Model):
    name = models.CharField(max_length = 20) #PGなど班の情報
    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    generation = models.IntegerField(blank=True)
    message = models.CharField(max_length = 140)
    intro = MarkdownxField('intro',blank=True)
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

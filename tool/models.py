from django.db import models
# マークダウン使用のため
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify

from mdeditor.fields import MDTextField

# Create your models here.
from account.models import User

# Create your models here.
class Tool(models.Model):
    name = models.CharField(max_length=30)
    icon = models.ImageField(upload_to='tool_icon/', default='defo')
    kind = models.CharField(max_length=15)
    intro = MDTextField('intro')
    editor = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name

    def formatted_markdown(self):
        return markdownify(self.intro) # モデルデータをMarkDown形式に変換してくれる



from django.db import models
from tool.models import Tool
from account.models import User
from member.models import UserTool
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
# Create your models here.

class Work(models.Model):
    name =  models.CharField(max_length=50)
    tool = models.ForeignKey(Tool,on_delete=models.CASCADE)
    user = models.ManyToManyField(User)
    leader = models.OneToOneField(User,on_delete=models.SET_NULL,null=True)
    main_image = models.ImageField(upload_to='work_main_image/', default='defo')
    intro = MarkdownxField('intro')
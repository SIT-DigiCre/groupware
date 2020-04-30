from django.db import models
from tool.models import Tool
from account.models import User
from member.models import UserTool
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
# Create your models here.

class Work(models.Model):
    name =  models.CharField(max_length=50)
    tools = models.ManyToManyField(Tool)
    users = models.ManyToManyField(User)
    leader_user_id = models.IntegerField(blank=True)
    main_image = models.ImageField(upload_to='work_main_image/', default='defo')
    intro = MarkdownxField('intro')
    STATUS_CHOICE =(
        ('planning','planning'),
        ('making','making'),
        ('finished','finished'),
    )
    status = models.CharField(max_length=10,choices=STATUS_CHOICE,default=0)
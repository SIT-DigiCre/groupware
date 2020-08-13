from django.db import models
from account.models import User
from django.core.validators import MinValueValidator

class Status(models.Model):
    name = models.CharField(max_length=10)
    order = models.IntegerField(default=1)
    is_completed = models.BooleanField(default=False)
    color = models.CharField(max_length=20, default="")

    class Meta:
        ordering = ('order',) # order順にする

    def __str__(self):
        return self.name

class Priority(models.Model):
    name = models.CharField(max_length=10, default="")
    color = models.CharField(max_length=20, default="")
    
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=10, default="")
    color = models.CharField(max_length=20, default="")

    def __str__(self):
        return self.name


class Issue(models.Model):
    title = models.CharField(verbose_name='表題', max_length=50)
    status = models.ForeignKey(Status, verbose_name='ステータス', on_delete=models.CASCADE)
    content = models.TextField(verbose_name='内容', blank=True)
    
    category = models.ForeignKey(Category, verbose_name='種別', on_delete=models.CASCADE)
    priority = models.ForeignKey(Priority, null=True, verbose_name='重要度', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='user', verbose_name='登録者', on_delete=models.CASCADE)
    assignee = models.ForeignKey(User, null=True, related_name='assignee', verbose_name='担当者', on_delete=models.CASCADE)
    
    created_at = models.DateTimeField(verbose_name='登録日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)

    class Meta:
        ordering = ('-created_at', ) # 新着順にする

    def __str__(self):
        return self.title

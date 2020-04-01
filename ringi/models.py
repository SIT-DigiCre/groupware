from django.db import models
from account.models import User
from django.core.validators import MinValueValidator

class Status(models.Model):
    state_type = models.CharField(max_length=10)
    order = models.IntegerField(default=1)
    is_completed = models.BooleanField(default=False)
    color = models.CharField(max_length=20, default="")

    class Meta:
        ordering = ('order',) # order順にする

    def __str__(self):
        return self.state_type

class Ringi(models.Model):
    title = models.CharField(verbose_name='タイトル', max_length=50)
    status = models.ForeignKey(Status, verbose_name='ステータス', on_delete=models.CASCADE)
    price = models.IntegerField(verbose_name='金額', validators=[MinValueValidator(0)])
    owner = models.ForeignKey(User, verbose_name='登録者', on_delete=models.CASCADE)
    created_at = models.DateTimeField(verbose_name='登録日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)
    purpose = models.CharField(verbose_name='目的', max_length=50, default='')
    note = models.TextField(verbose_name='備考', max_length=200, blank=True, default='')
    
    class Meta:
        ordering = ('-created_at',) # 新着順にする

    def __str__(self):
        return self.title

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

class Urgency(models.Model):
    urgency_type = models.CharField(max_length=10, default="", 
        help_text="通常: 1週間待つ、幹部通さないで稟議→反応→会計最終判断, 緊急: 1週間待てない、幹部１人の確認しました, 事後報告: 超緊急、当日中、プリンターインクなど")
    color = models.CharField(max_length=20, default="")
    
    def __str__(self):
        return self.urgency_type

class Ringi(models.Model):
    title = models.CharField(verbose_name='表題', max_length=50)
    status = models.ForeignKey(Status, verbose_name='ステータス', on_delete=models.CASCADE)
    price = models.PositiveIntegerField(verbose_name='金額', validators=[MinValueValidator(0)])
    owner = models.ForeignKey(User, verbose_name='登録者', on_delete=models.CASCADE)
    created_at = models.DateTimeField(verbose_name='登録日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)
    purpose = models.CharField(verbose_name='目的', max_length=50, default='')
    note = models.TextField(verbose_name='備考', max_length=200, blank=True, default='')
    urgency = models.ForeignKey(Urgency, verbose_name='緊急度', on_delete=models.CASCADE)
    is_purchased = models.BooleanField(verbose_name='購入済', default=False)
    is_pay_offed = models.BooleanField(verbose_name='精算済', default=False)
    receipt_image = models.ImageField(verbose_name='領収書', upload_to='receipt_image/', default='defo')

    class Meta:
        ordering = ('-urgency', '-created_at', ) # 緊急度、新着順にする

    def __str__(self):
        return self.title

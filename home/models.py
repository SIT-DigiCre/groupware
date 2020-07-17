from django.db import models
from account.models import User
# Create your models here.
class Notice(models.Model):
    to = models.ForeignKey(User,on_delete=models.CASCADE)
    text = models.CharField(max_length=30)
    link = models.CharField(max_length=30,blank=True,null=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_important = models.BooleanField(default=False)
    def __str__(self):
        return self.text

    def save(self, **kwargs):
        if self.is_active:
            #SlackDMへ送る
            pass
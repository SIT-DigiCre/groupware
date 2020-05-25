from django.db import models
from account.models import User
# マークダウン使用のため
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
# new md
from mdeditor.fields import MDTextField

class Channel(models.Model):
    name = models.CharField(max_length=64)
    icon_url = models.URLField(max_length=200,blank=True)
    # member = models.varchar(64)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Message(models.Model):
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = MDTextField('Contents')
    pub_date = models.DateTimeField(auto_now_add=True)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)

    class Meta:
        ordering = ('-pub_date',) # 新着順にする

    def __str__(self):
        return self.title


# Messageとの共通要素多い感じがします
class Reply(models.Model):
    parent = models.ForeignKey(Message, on_delete=models.CASCADE)
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    content = MDTextField('Contents')
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-pub_date',) # 新着順にする

    def __str__(self):
        return self.content

    def formatted_markdown(self):
        return markdownify(self.content) # モデルデータをMarkDown形式に変換してくれる


class Stamp(models.Model):
    name = models.CharField(max_length=64)
    image = models.ImageField(upload_to='stamp_img/', default='defo')
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class MessageStamp(models.Model):
    stamp = models.ForeignKey(Stamp,on_delete=models.CASCADE)
    message = models.ForeignKey(Message,on_delete=models.CASCADE)
    users = models.ManyToManyField(User)
    def __str__(self):
        return self.message.title +':'+self.stamp.name
    def return_names(self):
        names = ""
        for user in self.users.all():
            names += user.username + " "
        return names
class ReplyStamp(models.Model):
    stamp = models.ForeignKey(Stamp,on_delete=models.CASCADE)
    reply = models.ForeignKey(Reply,on_delete=models.CASCADE)
    users = models.ManyToManyField(User)
    def __str__(self):
        return self.stamp.name
    def return_names(self):
        names = ""
        for user in self.users.all():
            names += user.username + " "
        return names

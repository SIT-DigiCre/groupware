from django.db import models
from account.models import User


class Object(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    file_name = models.CharField(max_length=64)
    KIND_CHOICE = (
        ('other', 'other'),
        ('image', 'image'),
        ('video', 'video'),
        ('pptx', 'pptx'),
        ('pdf', 'pdf'),
        ('music', 'music'),
    )
    kind = models.CharField(max_length=10, choices=KIND_CHOICE, default=0)
    file_url = models.TextField()

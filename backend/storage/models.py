from django.db import models
from account.models import User


class FileObject(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    file_name = models.CharField(max_length=64)
    is_download_only = models.BooleanField(default=False)
    file_url = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

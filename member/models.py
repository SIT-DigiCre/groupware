from django.db import models
from account.models import User
from tool.models import Tool

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    generation = models.IntegerField()
    message = models.CharField(max_length = 140)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class UserTool(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE)
    level = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.tool.name
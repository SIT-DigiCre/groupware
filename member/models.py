from django.db import models
from account.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    generation = models.IntegerField()
    message = models.CharField(max_length = 140)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name

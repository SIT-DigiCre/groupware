from django.db import models
from account.models import User
from django.core.validators import MinValueValidator

class Status(models.Model):
    state_type = models.CharField(max_length=10)

    def __str__(self):
        return self.state_type

class Ringi(models.Model):
    title = models.CharField(max_length=100)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    price = models.IntegerField(validators=[MinValueValidator(0)])
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('-created_at',) # 新着順にする

    def __str__(self):
        return self.title

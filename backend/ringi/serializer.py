from django.db import models
from django.db.models.base import Model
from rest_framework import serializers
from .models import Ringi
from account.models import User

class RingiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ringi
        fields = ('title','status','price','owner',
                    'purpose','note','is_purchased',
                    'is_pay_offed')
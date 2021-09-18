from django.db import models
from rest_framework import serializers
from .models import FileObject


class FileObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileObject
        fields = ('id', 'user', 'file_name', 'kind', 'file_url', 'created_at')

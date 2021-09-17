from django.db import models
from rest_framework import serializers
from .models import WorkTag, WorkItem


class WorkTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkTag
        fields = ('name', 'intro')


class WorkItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkItem
        fields = ('name', 'intro', 'user', 'tools',
                  'tags', 'files', 'created_at')

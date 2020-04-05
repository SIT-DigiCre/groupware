from django import forms
from .models import *
from tool.models import Tool

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['message',]

class UserToolForm(forms.Form):
    tool = forms.ModelChoiceField(label='ツール',queryset=Tool.objects.all(),)
    
    level = forms.IntegerField()



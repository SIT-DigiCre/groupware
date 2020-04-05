from django import forms
from .models import *
from tool.models import Tool

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['message',]

class UserToolForm(forms.Form):
    
    c_tool = forms.CharField()
    level = forms.IntegerField()



from django import forms
from .models import *
from tool.models import Tool

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['message',]

class UserToolForm(forms.Form):
    TOOL = (('',''),)
    c_tools = Tool.objects.all()
    for t in c_tools:
        TOOL += ((t.name,t.name),)
    c_tool = forms.ChoiceField(choices=TOOL)
    level = forms.IntegerField()



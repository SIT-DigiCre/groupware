from django import forms
from .models import Tool

class ToolForm(forms.ModelForm):
    icon = forms.FileField()
    class Meta:
        model = Tool
        fields = ['name', 'icon','kind','intro',]


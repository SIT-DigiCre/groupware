from django import forms
from .models import *
from tool.models import Tool

class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
    class Meta:
        model = Profile
        fields = ['message','intro',]

class UserToolForm(forms.Form):
    tool = forms.ModelChoiceField(label='ツール',queryset=Tool.objects.all(),)
    
    level = forms.IntegerField()



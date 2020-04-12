from django import forms
from .models import Tool

class ToolForm(forms.ModelForm):
    icon = forms.ImageField()
    def __init__(self, *args, **kwargs):
        super(ToolForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
    class Meta:
        model = Tool
        fields = ['name', 'icon','kind','intro',]


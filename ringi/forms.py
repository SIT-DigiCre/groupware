from django import forms
from .models import Ringi

class RingiForm(forms.ModelForm):
    class Meta:
        model = Ringi
        fields = ['title', 'price']


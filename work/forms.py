from django import forms
from .models import Work

class WorkForm(forms.ModelForm):
    main_image = forms.FileField()
    class Meta:
        model = Work
        fields = ['name', 'tool','main_image','intro',]


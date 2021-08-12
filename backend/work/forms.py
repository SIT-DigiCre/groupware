from django import forms
from .models import Work

class WorkForm(forms.ModelForm):
    main_image = forms.FileField()
    def __init__(self, *args, **kwargs):
        super(WorkForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
    class Meta:
        model = Work
        fields = ['name','main_image','intro',]


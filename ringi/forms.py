from django import forms
from .models import Ringi

class RingiForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RingiForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Ringi
        fields = ['title', 'price', 'urgency', 'purpose', 'note', 'receipt_image']

class RingiEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RingiEditForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Ringi
        fields = ['status', 'is_purchased', 'is_pay_offed']

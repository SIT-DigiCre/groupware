from django import forms
from .models import Message, Reply


class NewThreadForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(NewThreadForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Message
        fields = ['channel', 'title', 'content']


class EditThreadForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EditThreadForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Message
        fields = ['content']


class ReplyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ReplyForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Reply
        fields = ['content']

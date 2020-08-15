from django import forms
from .models import Issue

class IssueForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(IssueForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Issue
        fields = ['title', 'category', 'content']

class IssueEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(IssueEditForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Issue
        fields = ['status', 'assignee', 'content']

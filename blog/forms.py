from django import forms
from .models import *

class NewArticleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(NewArticleForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
    class Meta:
        model = Article
        fields = ['title','content',]

class EditArticleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EditArticleForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
    class Meta:
        model = Article
        fields = ['title','content',]

class NewArticleTagForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(NewArticleTagForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
    class Meta:
        model = ArticleTag
        fields = ['name','content',]

class EditArticleTagForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EditArticleTagForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
    class Meta:
        model = ArticleTag
        fields = ['content',]

class EventArticleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EventArticleForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
    class Meta:
        model = EventArticle
        fields = ['article',]

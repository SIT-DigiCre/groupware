from django import forms
from .models import Article,ArticleTag

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
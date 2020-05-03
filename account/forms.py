from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

# ログインフォーム
class LoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label  # placeholderにフィールドのラベルを入れる

# ユーザー登録用フォーム
class UserCreateForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('email', 'last_name', 'first_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def clean_email(self):
        email = self.cleaned_data['email']
        if email[-17:] != 'shibaura-it.ac.jp':
            raise forms.ValidationError('登録はshibauraドメインにのみ制限されています！')
        
        User.objects.filter(email=email, is_active=False).delete() # すでに仮登録されている場合
        return email

class UserEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
    class Meta:
        model = User
        fields = ['icon','username',]
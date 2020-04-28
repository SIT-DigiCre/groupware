from django.contrib.auth.views import LoginView, LogoutView
from .forms import LoginForm

class Login(LoginView):
    form_class = LoginForm
    template_name = 'account/login.html'

class Logout(LogoutView):
    template_name = 'home/index.htm'

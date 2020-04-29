from django.contrib.auth.views import LoginView, LogoutView
from .forms import LoginForm
from django.core.mail import send_mail
from django.http import HttpResponse

class Login(LoginView):
    form_class = LoginForm
    template_name = 'account/login.html'

class Logout(LogoutView):
    template_name = 'home/index.htm'

def send_email(request):
    subject = "題名"
    message = "本文\\nです"
    user = request.user  # ログインユーザーを取得する
    from_email = 'sitdigicrecircle@gmail.com'  # 送信者
    user.email_user(subject, message, from_email)  # メールの送信

    return HttpResponse(str(user.email) + "にメール送信した！！！！")

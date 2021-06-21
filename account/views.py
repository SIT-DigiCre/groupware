
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.views import (
    LoginView,LogoutView,
    PasswordChangeView, PasswordChangeDoneView,
    PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView
)
from django.contrib.sites.shortcuts import get_current_site
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import generic

from .forms import (
    LoginForm,
    UserCreateForm,
    MyPasswordChangeForm,
    MyPasswordResetForm,
    MySetPasswordForm
)
from member.models import Profile

User = get_user_model()

class Login(LoginView):
    form_class = LoginForm
    template_name = 'account/login.html'

class Logout(LogoutView):
    template_name = 'account/logout.html'

# メール送信のテスト
def send_email(request):
    subject = "題名"
    message = "本文\\nです"
    user = request.user  # ログインユーザーを取得する
    from_email = 'sitdigicrecircle@gmail.com'  # 送信者
    user.email_user(subject, message, from_email)  # メールの送信

    return HttpResponse(str(user.email) + "にメール送信を行いました")

# ユーザー仮登録
class UserCreate(generic.CreateView):
    
    template_name = 'account/user_create.html'
    form_class = UserCreateForm

    # 仮登録と本登録用メールの発行
    def form_valid(self, form):
        # 仮登録と本登録の切り替えは、is_active属性を使う
        # 退会処理も、is_activeをFalseにする
        user = form.save(commit=False)
        user.is_active = False
        # 便宜的に、メールアドレスの最初の7文字を学生番号とみなし、ユーザーネームとする。
        user.username = user.email[:7]
        user.student_id = user.email[:7]
        user.save()
        profile = Profile()
        profile.user = user
        profile.message = "DefaultMessage"
        #mX -7 それ以外は-3
        student_kind = user.student_id[:1]
        student_join_num = int(user.student_id[2:4])
        if student_kind == 'm':
            student_join_num -= 7
        else:
            student_join_num -= 3
        profile.generation = student_join_num
        profile.save()

        # アクティベーションURLの送付
        current_site = get_current_site(self.request)
        domain = current_site.domain
        context = {
            'protocol': self.request.scheme,
            'domain': domain,
            'token': dumps(user.pk), # tokenを生成
            'user': user,
        }

        subject = render_to_string('account/mail_template/create/subject.txt', context)
        message = render_to_string('account/mail_template/create/message.txt', context)

        user.email_user(subject, message)
        return redirect('account:user_create_done')

# ユーザ仮登録完了
class UserCreateDone(generic.TemplateView):
    template_name = 'account/user_create_done.html'

# メール内URLアクセス後のユーザー本登録
class UserCreateComplete(generic.TemplateView):
    template_name = 'account/user_create_complete.html'
    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60*60*24)  # タイムアウトは1日

    # tokenが正しければ本登録
    def get(self, request, **kwargs):
        token = kwargs.get('token')
        try:
            user_pk = loads(token, max_age=self.timeout_seconds)

        # 期限切れ
        except SignatureExpired:
            return HttpResponseBadRequest()

        # tokenが間違っている
        except BadSignature:
            return HttpResponseBadRequest()

        # tokenは問題なし
        else:
            try:
                user = User.objects.get(pk=user_pk)
            except User.DoesNotExist:
                return HttpResponseBadRequest()
            else:
                if not user.is_active:
                    # 問題なければ本登録とする
                    user.is_active = True
                    user.save()
                    return super().get(request, **kwargs)

        return HttpResponseBadRequest()

# パスワード変更
class PasswordChange(PasswordChangeView):
    form_class = MyPasswordChangeForm
    success_url = reverse_lazy('account:password_change_done')
    template_name = 'account/password_change.html'

# パスワード変更完了
class PasswordChangeDone(PasswordChangeDoneView):
    template_name = 'account/password_change_done.html'

# パスワード変更用URLの送付ページ
class PasswordReset(PasswordResetView):
    subject_template_name = 'account/mail_template/password_reset/subject.txt'
    email_template_name = 'account/mail_template/password_reset/message.txt'
    template_name = 'account/password_reset_form.html'
    form_class = MyPasswordResetForm
    success_url = reverse_lazy('account:password_reset_done')

# パスワード変更用URLを送りましたページ
class PasswordResetDone(PasswordResetDoneView):
    template_name = 'account/password_reset_done.html'

# 新パスワード入力ページ
class PasswordResetConfirm(PasswordResetConfirmView):
    form_class = MySetPasswordForm
    success_url = reverse_lazy('account:password_reset_complete')
    template_name = 'account/password_reset_confirm.html'

# 新パスワード設定しましたページ
class PasswordResetComplete(PasswordResetCompleteView):
    template_name = 'account/password_reset_complete.html'
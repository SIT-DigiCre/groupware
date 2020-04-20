from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Channel,Message,Reply,Stamp
from .forms import NewThreadForm,ReplyForm,EditThreadForm

@login_required(login_url='/admin/login/')
def jump(request):
    ch_first = Channel.objects.first()
    return redirect(to='./' + ch_first.name)

@login_required(login_url='/admin/login/')
def index(request, channel_name, page=1):
    # GETアクセス時の処理
    if request.method == 'GET':
        channel_list = Channel.objects.all()
        channel_now = Channel.objects.filter(name=channel_name).first()
        messages = Message.objects.filter(channel=channel_now.id)
        data = Paginator(messages, 5) # 1ページに5つスレッドを表示
        params = {
            'channel_list': channel_list,
            'channel_name': channel_name,
            'messages': data.get_page(page),
            'form': NewThreadForm(),
        }
        return render(request, 'bbs/index.htm', params)

@login_required(login_url='/admin/login/')
def new_thread(request):
    if request.method == 'POST':
        obj = Message()
        obj.member = request.user
        message = NewThreadForm(request.POST, instance=obj)
        message.save()
        return redirect(to='/bbs')

# indexと共通要素多いです
@login_required(login_url='/admin/login/')
def show(request, channel_name, id=1):
    # 共通処理
    message = Message.objects.filter(id=id).first()

    # POSTアクセス時（返信時）の処理
    if request.method == 'POST':
        if 'edit-form' in request.POST and request.user == message.member:
            message_form = EditThreadForm(request.POST,instance=message)
            edit_post = message_form.save(commit=False)
            edit_post.member=request.user
            edit_post.channel=message.channel
            edit_post.title=message.title
            edit_post.save()

        elif 'reply-form' in request.POST:
            obj = Reply()
            obj.member = request.user
            obj.parent = message
            reply = ReplyForm(request.POST, instance=obj)
            reply.save()
        
        # 同じページにリダイレクトするだけなので、もっと賢い書き方あるはず
        return redirect(to='/bbs/' + channel_name + '/show/' + str(id)) 

    # GETアクセス時の処理
    channel_list = Channel.objects.all()
    replys = Reply.objects.all().filter(parent=message).reverse() # 古いものが上に
    params = {
        'channel_list': channel_list,
        'channel_name': channel_name,
        'message': message,
        'replys': replys,
        'form_reply':ReplyForm(),
        'form_edit':EditThreadForm(instance=message),
    }
    
    return render(request, 'bbs/show.htm', params)
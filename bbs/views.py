from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Channel,Message,Reply,Stamp,MessageStamp,ReplyStamp
from .forms import NewThreadForm,ReplyForm,EditThreadForm
from django_slack import slack_message
from .common import get_user_channel

@login_required()
def jump(request):
    ch_first = Channel.objects.first()
    return redirect(to='./' + ch_first.name)

@login_required()
def index(request, channel_name):
    # GETアクセス時の処理
    display_num = 5 # 1ページに表示するレコードの件数

    channel_list = get_user_channel(request)
    channel_now = Channel.objects.filter(name=channel_name).first()

    if 'search_word' in request.GET:
        word = request.GET['search_word']
        messages = Message.objects.filter(channel=channel_now.id).filter(Q(title__contains=word)|Q(content__contains=word))
        result_message = '「' + word + '」の検索結果（' + str(messages.count()) + '件）'
    else:
        messages = Message.objects.filter(channel=channel_now.id)
        result_message = 'すべてのスレッド（' + str(messages.count()) + '件）'

    data = Paginator(messages, display_num)
    page = request.GET.get('page')

    params = {
        'channel_list': channel_list,
        'channel_name': channel_name,
        'page_obj': data.get_page(page),
        'stamps':Stamp.objects.all(),
        'result_message': result_message, 
    }
    return render(request, 'bbs/index.htm', params)

# indexと共通要素多いです
@login_required()
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
    channel_list = get_user_channel(request)
    replys = Reply.objects.all().filter(parent=message).reverse() # 古いものが上に
    params = {
        'channel_list': channel_list,
        'channel_name': channel_name,
        'message': message,
        'replys': replys,
        'form_reply':ReplyForm(),
        'stamps':Stamp.objects.all(),
        'form_edit':EditThreadForm(instance=message),
    }
    
    return render(request, 'bbs/show.htm', params)

@login_required(login_url='/admin/login/')
def create(request):
    # POSTアクセス時（新規スレッド作成）の処理
    if request.method == 'POST':
        obj = Message()
        obj.member = request.user
        message = NewThreadForm(request.POST, instance=obj)
        message.save()

        # チャンネルがgeneralの場合はslackにも送信
        if request.POST['channel'] == 'general':
            attachments = [
                {
                    'title': request.POST['title'],
                    'text': request.POST['content'],
                },
            ]
            slack_message('bbs/slack_message.txt', {'owner': request.user.username}, attachments)
        return redirect(to='/bbs')

    params = {
        'form': NewThreadForm(),
    }
    return render(request, 'bbs/create.htm', params)

@login_required()
def edit(request, channel_name, id=1):
    # 共通処理
    message = Message.objects.filter(id=id).first()

    # POSTアクセス時（返信時）の処理
    if request.method == 'POST':
        if request.user == message.member:
            message_form = EditThreadForm(request.POST,instance=message)
            edit_post = message_form.save(commit=False)
            edit_post.member=request.user
            edit_post.channel=message.channel
            edit_post.title=message.title
            edit_post.save()
        # 同じページにリダイレクトするだけなので、もっと賢い書き方あるはず
        return redirect(to='/bbs/' + channel_name + '/show/' + str(id)) 

    params = {
        'channel_name': channel_name,
        'form':EditThreadForm(instance=message),
    }
    
    return render(request, 'bbs/edit.htm', params)

@login_required(login_url='/admin/login/')
def message_stamp(request,message_id,stamp_id):
    print('message_stamp')
    message = Message.objects.filter(id=message_id).first()
    stamp = Stamp.objects.filter(id=stamp_id).first()
    http = ""
    if len(message.messagestamp_set.filter(stamp=stamp).all()) != 0:
        if request.user in message.messagestamp_set.filter(stamp=stamp).first().users.all():
            print('stamp:'+str(stamp.id)+':user find!')
            tr_stmp = message.messagestamp_set.filter(stamp=stamp).first()
            tr_stmp.users.remove(request.user)
            if len(tr_stmp.users.all())==0:
                print('user:0')
                tr_stmp.delete()
        else:
            print('stamp:'+str(stamp.id)+':user not find!')
            message.messagestamp_set.filter(stamp=stamp).first().users.add(request.user)
    else:
        new_stamp = MessageStamp()
        new_stamp.message = message
        new_stamp.stamp = stamp
        new_stamp.save()
        new_stamp.users.add(request.user)
        new_stamp.save()
    message.save()
    message = Message.objects.filter(id=message_id).first()
    for st in message.messagestamp_set.all():
        tmp_http = '''
        <a id="btn_{0}" data-toggle="tooltip" title="{1}" href="javascript:void(0);" onclick="bbsStampOnClick('{2}',{3},'message');" class="badge badge-pill badge-secondary">
        <img src="{4}" alt="" style="width: 15px;height:15px;">{5}</a>
        '''.format(st.stamp.name,st.return_names(),str(st.stamp.id),message.id,st.stamp.image.url,str(len(st.users.all())))
        http += tmp_http
    return HttpResponse(http)

@login_required(login_url='/admin/login/')
def reply_stamp(request,reply_id,stamp_id):
    print('reply_stamp')
    reply = Reply.objects.filter(id=reply_id).first()
    stamp = Stamp.objects.filter(id=stamp_id).first()
    http = ""
    if len(reply.replystamp_set.filter(stamp=stamp).all()) != 0:
        if request.user in reply.replystamp_set.filter(stamp=stamp).first().users.all():
            print('stamp:'+str(stamp.id)+':user find!')
            tr_stmp = reply.replystamp_set.filter(stamp=stamp).first()
            tr_stmp.users.remove(request.user)
            if len(tr_stmp.users.all())==0:
                print('user:0')
                tr_stmp.delete()
        else:
            print('stamp:'+str(stamp.id)+':user not find!')
            reply.replystamp_set.filter(stamp=stamp).first().users.add(request.user)
    else:
        new_stamp = ReplyStamp()
        new_stamp.reply = reply
        new_stamp.stamp = stamp
        new_stamp.save()
        new_stamp.users.add(request.user)
        new_stamp.save()
    reply.save()
    reply = Reply.objects.filter(id=reply_id).first()
    for st in reply.replystamp_set.all():
        tmp_http = '''
        <a id="btn_{0}" data-toggle="tooltip" title="{1}" href="javascript:void(0);" onclick="bbsStampOnClick('{2}',{3},'reply');" class="badge badge-pill badge-secondary">
        <img src="{4}" alt="" style="width: 15px;height:15px;">{5}</a>
        '''.format(st.stamp.name,st.return_names(),str(st.stamp.id),reply.id,st.stamp.image.url,str(len(st.users.all())))
        http += tmp_http
    return HttpResponse(http)

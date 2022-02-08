from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator
from django.db.models import Count
from rest_framework import viewsets, status
from rest_framework.views import APIView

from backend.ringi.serializer import RingiSerializer
from .models import Ringi, Status
from .forms import RingiForm, RingiEditForm
from rest_framework.response import Response



@login_required()
def index(request):
    # GETアクセス時の処理
    display_num = 10 # 1ページに表示するレコードの件数
    
    if 'status' in request.GET:
        ringis = Ringi.objects.filter(status=request.GET['status'])
    else:
        ringis = Ringi.objects.all()
    
    ringis_page = Paginator(ringis, display_num)
    page = request.GET.get('page')

    params = {
        'title': '費用申請',
        'page_obj': ringis_page.get_page(page),
        'uncompleted_statuses': Status.objects.filter(is_completed=False),
        'records_num': ringis.count(),
    }
    return render(request, 'ringi/index.htm', params)

@login_required()
def create(request):
    params = {
        'title': '新規',
        'form': RingiForm()
    }
    # POSTアクセス時の処理
    if request.method == 'POST':
        obj = Ringi()
        obj.owner = request.user
        obj.status = Status.objects.all().first()
        ringi = RingiForm(request.POST,request.FILES, instance=obj)
        ringi.save()
        return redirect(to='/ringi')

    # GETアクセス時の処理
    return render(request, 'ringi/create.htm', params)

@login_required()
def show(request, id):
    params = {
        'title': '詳細',
        'ringi': Ringi.objects.get(id=id)
    }
    return render(request, 'ringi/show.htm', params)

@login_required()
@permission_required('ringi.change_ringi')
def edit(request, id):
    obj = Ringi.objects.get(id=id)
    # POSTアクセス時の処理
    if request.method == 'POST':
        ringi = RingiEditForm(request.POST, instance=obj)
        ringi.save()
        return redirect(to="/ringi")
    
    # GETアクセス時の処理
    params = {
        'title': '編集',
        'id': obj.id,
        'form': RingiEditForm(instance=obj)
    }
    return render(request, 'ringi/edit.htm', params)

@login_required()
@permission_required('ringi.delete_ringi')
def delete(request, id):
    ringi = Ringi.objects.get(id=id)
    # POSTアクセス時の処理
    if request.method == 'POST':
        ringi.delete()
        return redirect(to="/ringi")

    # GETアクセス時の処理
    params = {
        'title': '削除',
        'ringi': ringi
    }
    return render(request, 'ringi/delete.htm', params)

#========= REST API =====
"""
====== when create ======

必須
    receipt_image 領収書
    price 金額
    owner 登録者
    purpose 目的
    urgency 緊急度

任意
    note 備考

=========================


====== when delete ======

できるタイミング
    状況が申請中
    &
    未
        購入
        精算
    &
    リクエストユーザーが申請者

=========================
"""
#delte
class RingiView(APIView):
    def post(self, request, *args, **kwargs):
        """ 
        request.data データが入ってる
        """
        if 'title' not in request.data \
            or 'price' not in request.data \
            or 'owner' not in request.data \
            or 'purpose' not in request.data\
            or 'receipt_image' not in request.data \
            or 'urgency' not in request.data:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        

    def get(self,request,format=None):
        ringis = Ringi.objects.all()
        ringiserializer = RingiSerializer(ringis,many = True)
        return Response(ringiserializer.data)

    """ def delete():
        """

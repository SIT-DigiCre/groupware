from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from work.serializer import WorkItemSerializer, WorkTagSerializer
from django.shortcuts import *
from django.contrib.auth.decorators import login_required

from tool.models import *
from .models import *
from .forms import *

from rest_framework import viewsets, pagination
from home.permissions import IsOwnerOrReadOnlyUser


@login_required()
def index(request):
    works = Work.objects.all()
    params = {
        'works': works,
    }
    return render(request, 'work/index.htm', params)


@login_required()
def show(request, id):
    work = Work.objects.filter(id=id).first()
    params = {
        'work': work,
        'edit_enabled': request.user in work.users.all(),
    }
    return render(request, 'work/show.htm', params)


@login_required()
def edit(request, id):
    work = Work.objects.filter(id=id).first()
    if request.user in work.users.all():
        # POSTアクセス時（返信時）の処理
        if request.method == 'POST':
            if 'edit-work-form' in request.POST:
                work_form = WorkForm(
                    request.POST, request.FILES, instance=work)
                work_form.save()
            if 'edit-work-users-form' in request.POST:
                student_id = request.POST['student_id']
                print(student_id)
                user = User.objects.filter(student_id=student_id)
                if len(user.all()) != 0:
                    if user not in work.users.filter(id=user.id):
                        work.users.add(user.first())
            if 'edit-work-tools-form' in request.POST:
                tool_choice = request.POST['toolchoice']
                tool = Tool.objects.filter(id=tool_choice).first()
                work.tools.add(tool)
            return redirect(to='/work/'+str(work.id))
        params = {
            'work': work,
            'form': WorkForm(instance=work),
            'tools': Tool.objects.all(),
        }
        return render(request, 'work/edit.htm', params)

    return render(request, 'work/permission_erorr.htm')


@login_required()
def create(request):
    work = Work()
    if request.method == 'POST':
        work_form = WorkForm(request.POST, request.FILES, instance=work)
        work = work_form.save(commit=False)
        work.leader_user_id = request.user.id
        work.save()
        work.users.add(request.user)
        work.save()
        return redirect(to='/work/'+str(work.id))
    params = {
        'work': work,
        'form': WorkForm(),
    }
    return render(request, 'work/create.htm', params)


# REST_API

class WorkItemResultsPagination(pagination.PageNumberPagination):
    page_size = 15


class WorkItemViewSet(viewsets.ModelViewSet):
    queryset = WorkItem.objects.order_by('-created_at')
    serializer_class = WorkItemSerializer
    pagination_class = WorkItemResultsPagination
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        return serializer.save(user=self.request.user)


class WorkTagViewSet(viewsets.ModelViewSet):
    queryset = WorkTag.objects.all()
    serializer_class = WorkTagSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

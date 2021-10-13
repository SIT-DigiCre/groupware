import base64
import uuid
import os
from digigru.local_settings import CONOHA_IDENTITY_SERVER_URL, CONOHA_OBJECT_STRAGE_SERVER_URL
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from home.permissions import IsOwnerOrReadOnlyUser
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from . import object_strage
from .serializer import FileObjectSerializer
from .models import FileObject
from django.conf import settings


class FileObjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FileObject.objects.all()
    serializer_class = FileObjectSerializer
    permission_classes = (IsAuthenticated,)

class MyFileObjectViewSet(viewsets.ModelViewSet):
    queryset = FileObject.objects.all()
    serializer_class = FileObjectSerializer
    permission_classes = (IsOwnerOrReadOnlyUser,)
    def get_queryset(self):
        return FileObject.objects.filter(user=self.request.user).order_by('-created_at')
    def perform_update(self, serializer):
        return serializer.save(user=self.request.user)
    def perform_destroy(self, instance):
        object_strage.deleteObject(instance.file_url)
        return super().perform_destroy(instance)


class UploadFileObjectView(APIView):
    def post(self, request, *args, **kwargs):
        if 'file_name' not in request.data or 'file' not in request.data or 'target_container' not in request.data or 'is_download_only' not in request.data:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        temp_file_name = str(uuid.uuid4()) + \
            os.path.splitext(request.data['file_name'])[1]
        if not os.path.exists('upload_temp'):
            os.mkdir('upload_temp')
        with open('upload_temp/'+temp_file_name, 'bw')as f:
            f.write(base64.b64decode(request.data['file']))
        target_container = 'TEST_'+request.data['target_container'] if settings.DEBUG else request.data['target_container']
        file_url = '{0}/{1}/{2}'.format(CONOHA_OBJECT_STRAGE_SERVER_URL,
                                        target_container, temp_file_name)
        upload_response = object_strage.uploadObject(
            'upload_temp/'+temp_file_name, target_container, temp_file_name)
        if upload_response.status_code != 201:
            os.remove('upload_temp/'+temp_file_name)
            return Response({"error": "なんかファイル作成失敗"+str(upload_response.content)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        fileObject = FileObject(
            user=request.user, file_name=request.data['file_name'], is_download_only=request.data['is_download_only'], file_url=file_url)
        fileObject.save()
        os.remove('upload_temp/'+temp_file_name)
        return Response({'id': fileObject.id, 'file_name': fileObject.file_name, 'is_download_only': fileObject.is_download_only, 'file_url': fileObject.file_url}, status=status.HTTP_201_CREATED)

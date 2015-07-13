# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from rest_framework import generics
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .models import ArchiveFile
from .serializers import ArchiveFileSerializer
from .serializers import UserSerializer
from .permissions import IsOwnerOrReadOnly


class IndexView(ListView):

    model = ArchiveFile
    template_name = 'ict_archive/index.html'


class ArchiveFileDetailView(DetailView):

    model = ArchiveFile


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('ict_archive:api-user-list', request=request, format=format),
        'files': reverse('ict_archive:api-archivefile-list', request=request, format=format)
    })


@api_view(['GET'])
def api_check_md5(request, format=None):
    """Проверяет, есть ли указанный MD5 в базе."""
    FILE_PRESENT = 1
    FILE_NOT_PRESENT = 0
    if ArchiveFile.objects.filter(md5Checksum=request.query_params.get('md5', False)):
        # Файл с таким MD5 есть в базе
        return Response({"status": FILE_PRESENT,
                         "message": "File with specified MD5 checksum exists in the archive."})
    else:
        # Файла с таким MD5 в базе нет
        return Response({"status": FILE_NOT_PRESENT,
                         "message": "File with specified MD5 checksum does not exist in the archive."})


class ApiUserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ApiUserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ApiArchiveFileList(generics.ListCreateAPIView):
    """List all `ArchiveFile`s, or create a new ArchiveFile."""
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = ArchiveFile.objects.all()
    serializer_class = ArchiveFileSerializer

    def perform_create(self, serializer):
        serializer.save(entryWriter=self.request.user)


class ApiArchiveFileDetail(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a ArchiveFile instance."""
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)
    queryset = ArchiveFile.objects.all()
    serializer_class = ArchiveFileSerializer

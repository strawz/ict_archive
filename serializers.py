from rest_framework import serializers

from ict_archive.models import ArchiveFile
from django.contrib.auth.models import User


class ArchiveFileSerializer(serializers.ModelSerializer):
    entryWriter = serializers.ReadOnlyField(source='entryWriter.username')

    class Meta:
        model = ArchiveFile


class UserSerializer(serializers.ModelSerializer):
    archive_files = serializers.PrimaryKeyRelatedField(many=True,
                                                       queryset=ArchiveFile.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'archive_files')

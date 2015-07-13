from django.contrib import admin

from .models import ArchiveFile, Tag


admin.site.register(ArchiveFile)
admin.site.register(Tag)
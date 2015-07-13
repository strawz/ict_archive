# -*- coding: utf-8 -*-
from django.db import models
# from django.contrib.auth.models import User


class ArchiveFile(models.Model):
    """
    Модель, описывающая файл в базе архива.
    Имена полей совпадают с полями метаданных Google Drive, где это возможно.
    """
    entryWriter = models.ForeignKey('auth.User', related_name='archive_files',
                                    blank=True, default=None,
                                    help_text="Пользователь-автор записи в базе данных")
    
    filePath = models.CharField(max_length=116, help_text="Путь к файлу в папке Inbox")
    md5Checksum = models.CharField(max_length=32, help_text="MD5 хэш-сумма файла")
    googleDriveFileId = models.CharField(blank=True, max_length=255, help_text="ID файла на Google Drive")
    fileSize = models.BigIntegerField(blank=True, null=True, help_text="Размер файла в байтах")
    webContentLink = models.URLField(blank=True, help_text= \
                                    "Ссылка для скачивания файла из браузера")
    mimeType = models.CharField(blank=True, max_length=255, help_text="MIME-тип файла")
    
    videoWidth = models.IntegerField(blank=True, null=True,
                                     help_text= "Ширина видео в пикселях")
    videoHeight = models.IntegerField(blank=True, null=True,
                                      help_text="Высота видео в пикселях")
    videoDuration = models.BigIntegerField(blank=True, null=True,
                                           help_text="Продолжительность видео в милисекундах")
    
    place = models.CharField(blank=True, max_length=255, help_text='Тег "Место"')
    event = models.CharField(blank=True, max_length=255, help_text='Тег "Событие"')
    person = models.CharField(blank=True, max_length=255, help_text='Тег "Человек"')
    timestamp = models.DateTimeField(blank=True, null=True, help_text='Тег "Время"')
    album = models.CharField(blank=True, max_length=255, help_text='Тег "Альбом"')
    
    SOURCE = 'SO'
    DRAFT = 'DR'
    MOVIE = 'MO'
    BROADCAST = 'BC'
    STATUS_CHOICES = (
        (SOURCE, 'Исходник'),
        (DRAFT, 'Черновик'),
        (MOVIE, 'Готовый фильм'),
        (BROADCAST, 'Запись прямого эфира'),
        ('', 'Без статуса')
    )
    status = models.CharField(blank=True, max_length=2, choices=STATUS_CHOICES,
                              help_text="Статус файла")

    # У файла могут быть копии в более высоком/низком качестве
    copies = models.ManyToManyField('self', blank=True, default=None, help_text="Копии файла")
    duplicate = models.CharField(blank=True, max_length=255,
                help_text="Ссылка на дубликат и отрезок совпадающего времени в ролике")
    favorite = models.BooleanField(default=False, help_text='Находится ли файл в "Избранном"')

    def __unicode__(self):
        return unicode(self.id)


class Tag(models.Model):
    """
    Модель, описывающая свободные теги для файлов в архиве.
    """
    archive_file = models.ManyToManyField(ArchiveFile, related_name="tags",
        related_query_name="tag")
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return unicode(self.name)

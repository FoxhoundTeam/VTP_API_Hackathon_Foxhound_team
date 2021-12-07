import json
import os
from uuid import uuid4
from django.db import models

class AllowedFile(models.Model):
    # TODO дополнить типы файлов

    SIZE_BYTE = 1
    SIZE_KBYTE = 1024
    SIZE_MBYTE = 1024**2
    SIZE_GBYTE = 1024**3
    SIZE_TBYTE = 1024**4

    SIZES = [
        (SIZE_BYTE, 'byte'),
        (SIZE_KBYTE, 'KB'),
        (SIZE_MBYTE, 'MB'),
        (SIZE_GBYTE, 'GB'),
        (SIZE_TBYTE, 'TB'),
    ]

    TYPE_XML = 'xml'
    TYPE_JSON = 'json'
    TYPE_PDF = 'pdf'
    TYPE_EXE = 'exe'
    TYPE_ZIP = 'zip'

    TYPES = [
        (TYPE_XML, 'xml'),
        (TYPE_JSON, 'json'),
        (TYPE_PDF, 'pdf'),
        (TYPE_EXE, 'exe'),
        (TYPE_ZIP, 'zip'),
    ]

    dttm_added = models.DateTimeField(auto_now_add=True)
    dttm_modified = models.DateTimeField(auto_now=True)
    max_depth = models.IntegerField(null=True, blank=True)
    max_size = models.IntegerField(null=True, blank=True)
    size_mul = models.IntegerField(choices=SIZES, default=SIZE_BYTE)
    file_type = models.CharField(max_length=8, choices=TYPES)

    @property
    def real_max_size(self):
        return self.max_size * self.size_mul if self.max_size else None

def content_file_name(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid4(), ext)
    return os.path.join('files', filename)

class FileInfo(models.Model):
    STATUS_IN_PROGRESS = 'P'
    STATUS_OK = 'O'
    STATUS_ERROR = 'E'
    STATUS_VIOLATION = 'V'

    STATUSES = [
        (STATUS_ERROR, 'Ошибка'),
        (STATUS_IN_PROGRESS, 'В процессе'),
        (STATUS_OK, 'Ок'),
        (STATUS_VIOLATION, 'Нарушение'),
    ]

    name = models.CharField(max_length=1024)
    file = models.FileField(upload_to=content_file_name)
    dttm_loaded = models.DateTimeField(auto_now_add=True)
    dttm_end_check = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=1, choices=STATUSES, default=STATUS_IN_PROGRESS)
    message = models.TextField(null=True, blank=True)
    source = models.CharField(max_length=1024)
    client = models.TextField()
    file_type = models.CharField(max_length=8, default='Unknown')

class FilesProxy(models.Model):
    proxy_url = models.CharField(max_length=1024)
    headers = models.TextField(default='{}')

    def save(self, *args, **kwargs):
        if isinstance(self.headers, dict):
            self.headers = json.dumps(self.headers)
        super().save(*args, **kwargs)

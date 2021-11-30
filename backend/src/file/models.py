from django.db import models

class HTTPAllowedType(models.Model):
    # TODO дополнить модель
    name = models.CharField(max_length=512)
    code = models.CharField(max_length=512)
    dttm_added = models.DateTimeField(auto_now_add=True)
    dttm_modified = models.DateTimeField(auto_now=True)
    type = models.CharField(max_length=64)

class FileInfo(models.Model):
    STATUS_IN_PROGRESS = 'P'
    STATUS_OK = 'O'
    STATUS_ERROR = 'E'

    STATUSES = [
        (STATUS_ERROR, 'Ошибка'),
        (STATUS_IN_PROGRESS, 'В процессе'),
        (STATUS_OK, 'Ок')
    ]

    name = models.CharField(max_length=1024)
    file = models.FileField(upload_to='files')
    code = models.CharField(max_length=40, primary_key=True)
    status = models.CharField(max_length=1, choices=STATUSES, default=STATUS_IN_PROGRESS)
    message = models.TextField(null=True, blank=True)
    source = models.CharField(max_length=1024)
    client = models.TextField()

class FilesProxy(models.Model):
    proxy_url = models.CharField(max_length=1024)

from django.contrib import admin
from src.file.models import HTTPAllowedType, FileInfo, FilesProxy

admin.site.register(HTTPAllowedType)
admin.site.register(FilesProxy)
admin.site.register(FileInfo)

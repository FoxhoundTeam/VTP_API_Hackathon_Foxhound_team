from django.contrib import admin
from src.file.models import AllowedFile, FileInfo, FilesProxy

admin.site.register(AllowedFile)
admin.site.register(FilesProxy)
admin.site.register(FileInfo)

from django.conf.urls import url, include
from rest_framework import routers
from src.file.views import (
    AllowedFileViewSet,
    FileInfoViewSet,
    FilesProxyViewSet,
)

router = routers.DefaultRouter()
router.register(r'file', FileInfoViewSet, basename='FileInfo')
router.register(r'files_proxy', FilesProxyViewSet, basename='FilesProxy')
router.register(r'allowed_file', AllowedFileViewSet, basename='HTTPAllowedType')


urlpatterns = [
    url(r'^', include(router.urls)),
]
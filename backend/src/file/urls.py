from django.conf.urls import url, include
from rest_framework import routers
from src.file.views import (
    HTTPAllowedTypeViewSet,
    FileInfoViewSet,
    FilesProxyViewSet,
)

router = routers.DefaultRouter()
router.register(r'file', FileInfoViewSet, basename='FileInfo')
router.register(r'files_proxy', FilesProxyViewSet, basename='FilesProxy')
router.register(r'http_allowed_type', HTTPAllowedTypeViewSet, basename='HTTPAllowedType')


urlpatterns = [
    url(r'^', include(router.urls)),
]
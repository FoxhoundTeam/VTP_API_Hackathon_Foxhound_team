from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from src.file.models import (
    HTTPAllowedType, 
    FileInfo,
    FilesProxy,
)
from src.file.serializers import ( 
    HTTPAllowedTypeSerializer, 
    FileInfoSerializer,
    FilesProxySerializer,
)

class FileInfoViewSet(viewsets.ModelViewSet):
    queryset = FileInfo.objects.all()
    serializer_class = FileInfoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,]

    @action(detail=False, methods=['get'])
    def stats(self, request):

        return Response(
            {
                'count': FileInfo.objects.count(),
            }
        )

class HTTPAllowedTypeViewSet(viewsets.ModelViewSet):
    queryset = HTTPAllowedType.objects.all()
    serializer_class = HTTPAllowedTypeSerializer
    permission_classes = [IsAdminUser,]

    @action(detail=False, methods=['get'])
    def stats(self, request):

        return Response(
            {
                'count': HTTPAllowedType.objects.count(),
            }
        )

class FilesProxyViewSet(viewsets.ModelViewSet):
    queryset = FilesProxy.objects.all()
    serializer_class = FilesProxySerializer
    permission_classes = [IsAdminUser,]

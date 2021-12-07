import pandas as pd
from datetime import timedelta
from django.db.models import DateTimeField, Count, F, DateField
from django.db.models.functions import TruncHour, TruncDate
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from src.file.models import (
    AllowedFile, 
    FileInfo,
    FilesProxy,
)
from src.file.serializers import ( 
    AllowedFileSerializer, 
    FileInfoSerializer,
    FilesProxySerializer,
)
from src.websocket.serializers import ChartSerializer
from src.file.filters import FileInfoFilterSet

class FileInfoViewSet(viewsets.ModelViewSet):
    queryset = FileInfo.objects.all()
    serializer_class = FileInfoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,]
    filterset_class = FileInfoFilterSet

    @action(detail=False, methods=['get'])
    def chart(self, request):
        data = ChartSerializer(data=request.query_params)
        data.is_valid(raise_exception=True)
        data = data.validated_data
        dt_from = data['dt_from']
        dt_to = data['dt_to']
        violations = FileInfo.objects.filter(
            dttm_loaded__date__gte=dt_from, 
            dttm_loaded__date__lte=dt_to,
            status=FileInfo.STATUS_VIOLATION,
        )
        count = violations.count()
        freq = '1d'
        if dt_from == dt_to:
            freq = '1h'
            violations = violations.annotate(
                dttm_g=TruncHour('dttm_loaded', output_field=DateTimeField()),
            )
        else:
            violations = violations.annotate(
                dttm_g=TruncDate('dttm_loaded', output_field=DateField()),
            )
        data = list(
            violations.values('dttm_g').annotate(
                y=Count('*'),
                x=F('dttm_g'),
            ).order_by('x').values(
                'y',
                'x',
            )
        )
        if dt_from == dt_to:
            dt_to += timedelta(1)
        dttms = pd.date_range(dt_from, dt_to, freq=freq)
        if freq == '1d':
            dttms = dttms.date
        df = pd.DataFrame(data=dttms, columns=['x'])
        df.set_index('x', inplace=True)

        df = df.merge(pd.DataFrame(data=data, columns=['x', 'y']).set_index('x'), how='left', on='x')

        data = df.reset_index().fillna(0).to_dict('records')

        return Response(
            {
                'count': count,
                'data': data,
            }
        )

class AllowedFileViewSet(viewsets.ModelViewSet):
    queryset = AllowedFile.objects.all()
    serializer_class = AllowedFileSerializer
    permission_classes = [IsAdminUser,]

    @action(detail=False, methods=['get'])
    def stats(self, request):

        return Response(
            {
                'count': AllowedFile.objects.count(),
            }
        )
    

class FilesProxyViewSet(viewsets.ModelViewSet):
    queryset = FilesProxy.objects.all()
    serializer_class = FilesProxySerializer
    permission_classes = [IsAdminUser,]

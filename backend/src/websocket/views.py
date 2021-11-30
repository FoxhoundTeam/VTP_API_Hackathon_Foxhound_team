from datetime import timedelta
from django.db.models import DateTimeField, Count, F, DateField
from django.db.models.functions import TruncHour, TruncDate
import pandas as pd
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from src.websocket.filters import ViolationFilterSet
from src.websocket.models import (
    WebSocketSchema, 
    WebSocketViolation, 
    WebSocketCallback,
    WebSocketAllowedOrigin,
)
from src.websocket.serializers import (
    ChartSerializer, 
    WebSocketSchemaSeializer, 
    WebSocketViolationSerializer, 
    WebSocketCallbackSerializer,
    WebSocketAllowedOriginSerializer,
)

class WebSocketSchemaViewSet(viewsets.ModelViewSet):
    queryset = WebSocketSchema.objects.all()
    serializer_class = WebSocketSchemaSeializer
    permission_classes = [IsAdminUser,]

    @action(detail=False, methods=['get'])
    def stats(self, request):

        return Response(
            {
                'count': WebSocketSchema.objects.count(),
            }
        )


class WebSocketViolationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = WebSocketViolation.objects.all().order_by('-dttm')
    serializer_class = WebSocketViolationSerializer
    filterset_class = ViolationFilterSet
    permission_classes = [IsAdminUser,]

    @action(detail=False, methods=['get'])
    def chart(self, request):
        data = ChartSerializer(data=request.query_params)
        data.is_valid(raise_exception=True)
        data = data.validated_data
        dt_from = data['dt_from']
        dt_to = data['dt_to']
        violations = WebSocketViolation.objects.filter(dttm__date__gte=dt_from, dttm__date__lte=dt_to)
        count = violations.count()
        freq = '1d'
        if dt_from == dt_to:
            freq = '1h'
            violations = violations.annotate(
                dttm_g=TruncHour('dttm', output_field=DateTimeField()),
            )
        else:
            violations = violations.annotate(
                dttm_g=TruncDate('dttm', output_field=DateField()),
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

class WebSocketCallbackViewSet(viewsets.ModelViewSet):
    queryset = WebSocketCallback.objects.all()
    serializer_class = WebSocketCallbackSerializer
    permission_classes = [IsAdminUser,]

class WebSocketAllowedOriginViewSet(viewsets.ModelViewSet):
    queryset = WebSocketAllowedOrigin.objects.all()
    serializer_class = WebSocketAllowedOriginSerializer
    permission_classes = [IsAdminUser,]

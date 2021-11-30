import json
from src.websocket.models import (
    WebSocketSchema, 
    WebSocketViolation, 
    WebSocketCallback,
    WebSocketAllowedOrigin,
)
from rest_framework import serializers

class WebSocketSchemaSeializer(serializers.ModelSerializer):
    schema = serializers.JSONField()
    class Meta:
        model = WebSocketSchema
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['schema'] = instance.schema_value
        return data

class WebSocketViolationSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebSocketViolation
        fields = '__all__'

class WebSocketAllowedOriginSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebSocketAllowedOrigin
        fields = '__all__'

class WebSocketCallbackSerializer(serializers.ModelSerializer):
    headers = serializers.JSONField()
    class Meta:
        model = WebSocketCallback
        fields = '__all__'
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['headers'] = json.loads(instance.headers)
        return data

class ChartSerializer(serializers.Serializer):
    dt_from = serializers.DateField()
    dt_to = serializers.DateField()
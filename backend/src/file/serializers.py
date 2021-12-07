import json
from src.file.models import (
    AllowedFile, 
    FilesProxy,
    FileInfo,
)
from rest_framework import serializers
from django.conf import settings

from src.file.tasks import check_file, send_file_link_to_proxy

class AllowedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllowedFile
        fields = '__all__'

class FileInfoSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()
    name = serializers.CharField(read_only=True)
    source = serializers.CharField(read_only=True)
    client = serializers.CharField(read_only=True)
    file = serializers.FileField(write_only=True)

    def get_file_url(self, obj: FileInfo):
        return settings.EXTERNAL_HOST + obj.file.url

    class Meta:
        model = FileInfo
        fields = '__all__'

    def create(self, validated_data):
        validated_data['name'] = validated_data['file']
        request = self.context['request']
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        validated_data['source'] = ip
        validated_data['client'] = f"{request.user.id} {request.user.username}"
        instance = super().create(validated_data)
        check_file.delay(instance.id)
        send_file_link_to_proxy.delay(instance.id)
        return instance

class FilesProxySerializer(serializers.ModelSerializer):
    headers = serializers.JSONField()
    class Meta:
        model = FilesProxy
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['headers'] = json.loads(instance.headers)
        return data

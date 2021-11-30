from src.file.models import (
    HTTPAllowedType, 
    FilesProxy,
    FileInfo,
)
from rest_framework import serializers
from django.conf import settings

from src.file.tasks import check_file, send_file_link_to_proxy

class HTTPAllowedTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HTTPAllowedType
        fields = '__all__'

class FileInfoSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    def get_file_url(self, obj: FileInfo):
        return settings.EXTERNAL_HOST + obj.file.url

    class Meta:
        model = FileInfo
        fields = '__all__'

    def create(self, validated_data):
        instance = super().create(validated_data)
        check_file.delay(instance.code)
        send_file_link_to_proxy.delay(instance.code)
        return instance

class FilesProxySerializer(serializers.ModelSerializer):
    class Meta:
        model = FilesProxy
        fields = '__all__'

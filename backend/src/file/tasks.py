import requests

from src.celery.celery import app
from src.file.models import FileInfo, FilesProxy
from django.conf import settings


@app.task
def check_file(code):
    file_obj = FileInfo.objects.get(code=code)

    file = file_obj.file

    # do some check stuff

    file_obj.status = FileInfo.STATUS_OK
    file_obj.save()
    
@app.task
def send_file_link_to_proxy(file_code):
    for proxy in FilesProxy.objects.all():
        requests.post(
            proxy.proxy_url, 
            json={'url': f'{settings.EXTERNAL_HOST.rstrip("/")}/rest_api/file/{file_code}/'}
        )


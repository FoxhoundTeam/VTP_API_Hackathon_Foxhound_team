import json
import requests
from datetime import datetime, timedelta

from src.celery.celery import app
from src.file.models import FileInfo, FilesProxy
from django.conf import settings


@app.task
def check_file(id):
    file_obj = FileInfo.objects.get(id=id)
    status = FileInfo.STATUS_OK

    try:
        file = file_obj.file
        # do some check stuff
    except:
        status = FileInfo.STATUS_ERROR

    file_obj.status = status
    file_obj.dttm_end_check = datetime.now()
    file_obj.save()
    send_file_link_to_proxy(file_obj.id, status=status)
    
@app.task
def send_file_link_to_proxy(id, status='P'):
    for proxy in FilesProxy.objects.all():
        requests.post(
            proxy.proxy_url, 
            json={'url': f'{settings.EXTERNAL_HOST.rstrip("/")}/rest_api/file/{id}/', 'status': status},
            headers=json.loads(proxy.headers)
        )


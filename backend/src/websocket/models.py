import json
from django.db import models

class WebSocketSchema(models.Model):
    name = models.CharField(max_length=512)
    code = models.CharField(max_length=512, null=True, blank=True)
    dttm_added = models.DateTimeField(auto_now_add=True)
    dttm_modified = models.DateTimeField(auto_now=True)
    schema = models.TextField(default='{"type":"object"}')
    method = models.CharField(max_length=1024)

    @property
    def schema_value(self):
        if isinstance(self.schema, dict):
            return self.schema
        try:
            return json.loads(self.schema)
        except:
            return {"type":"object"}

    def save(self, *args, **kwargs):
        self.schema = json.dumps(self.schema_value)
        super().save(*args, **kwargs)

class WebSocketViolation(models.Model):
    TYPE_BAD_ORIGIN = 'BO'
    TYPE_BAD_METHOD = 'BM'
    TYPE_SQL_INJECTION = 'SI'
    TYPE_XSS = 'X'
    TYPE_BAD_WORD = 'BW'
    TYPE_INVALID_FORMAT = 'IF'
    TYPE_UNKNOWN_ECXEPTION = 'U'

    TYPES = [
        (TYPE_BAD_ORIGIN, 'Bad origin'),
        (TYPE_BAD_METHOD, 'Bad method'),
        (TYPE_SQL_INJECTION, 'SQL injection'),
        (TYPE_XSS, 'XSS attack'),
        (TYPE_BAD_WORD, 'Bad word'),
        (TYPE_INVALID_FORMAT, 'Invalid message format'),
        (TYPE_UNKNOWN_ECXEPTION, 'Unknown exception'),
    ]

    dttm = models.DateTimeField()
    dttm_added = models.DateTimeField(auto_now_add=True)
    dttm_modified = models.DateTimeField(auto_now=True)
    message = models.TextField(null=True, blank=True)
    error_message = models.TextField(null=True, blank=True)
    source = models.CharField(max_length=1024)
    client = models.TextField()
    type = models.CharField(max_length=2, choices=TYPES, default=TYPE_UNKNOWN_ECXEPTION)

class WebSocketCallback(models.Model):

    method = models.CharField(max_length=512)
    callback_url = models.CharField(max_length=1024)
    headers = models.TextField(default='{}')

    def save(self, *args, **kwargs):
        if isinstance(self.headers, dict):
            self.headers = json.dumps(self.headers)
        super().save(*args, **kwargs)

class WebSocketAllowedOrigin(models.Model):
    name = models.CharField(max_length=1024)

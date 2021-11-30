from django.contrib import admin
from src.websocket.models import (
    WebSocketViolation, 
    WebSocketSchema, 
    WebSocketAllowedOrigin,
    WebSocketCallback,
)


admin.site.register(WebSocketViolation)
admin.site.register(WebSocketSchema)
admin.site.register(WebSocketAllowedOrigin)
admin.site.register(WebSocketCallback)


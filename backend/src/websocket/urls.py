from django.conf.urls import url, include
from rest_auth.views import LoginView, UserDetailsView, LogoutView
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from src.websocket.views import (
    WebSocketSchemaViewSet,
    WebSocketViolationViewSet,
    WebSocketCallbackViewSet,
    WebSocketAllowedOriginViewSet,
)

rest_auth_urls = [
    url(r'^login/$', LoginView.as_view(), name='rest_login'),
    url(r'^logout/$', LogoutView.as_view(), name='rest_logout'),
    url(r'^user/$', UserDetailsView.as_view(), name='user'),
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^api-token-refresh/', refresh_jwt_token),
]

router = routers.DefaultRouter()
router.register(r'web_socket_schema', WebSocketSchemaViewSet, basename='WebSocketSchema')
router.register(r'web_socket_callback', WebSocketCallbackViewSet, basename='WebSocketCallback')
router.register(r'web_socket_allowed_origin', WebSocketAllowedOriginViewSet, basename='WebSocketAllowedOrigin')
router.register(r'violation', WebSocketViolationViewSet, basename='WebSocketViolation')


urlpatterns = [
    url(r'^auth/', include((rest_auth_urls, 'auth'), namespace='auth')),
    url(r'^', include(router.urls)),
]
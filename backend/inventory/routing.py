from django.urls import path

from inventory.consumers import AppConsumer

websocket_urlpatterns = [
    path('ws/main_page/', AppConsumer.as_asgi())
]

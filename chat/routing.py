from django.urls import path
from . import consumers  # views.py와 consumers.py는 비슷하게 작동(컨트롤러처럼)


websocket_urlpatterns = [
    # https는 wss, http는 ws로 작성
    path('wss/char/<str:room_id>/', consumers.ChatConsumer),
]

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import *
import json
import logging
from django.contrib.auth import get_user_model


class ChatConsumer(WebsocketConsumer):
    # websocket 연결 시 실행
    def connect(self):
        logger = logging.getLogger(__name__)
        # logger.error('======connect======')
        # logger.error('======self======' + self.__class__.__name__)
        
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_channel_layer_group = self.room_id

        # 소비자들은 비동기 channel layer 메서드를 호출할 때 동기적으로 받아야 하기 때문에 
        # async_to_sync(...) 같은 wrapper가 필요하다. (모든 channel layer 메서드는 비동기이다.)
        # self.channel_layer.group_add : 그룹에 join
        async_to_sync(self.channel_layer.group_add)(
            self.room_channel_layer_group,
            self.channel_name
        )
        
        # WebSocket 연결
        self.accept()

        messages = Message.objects.filter(room_id=self.room_id)

        for message in messages:
            self.send(text_data=json.dumps({
                'user_id': message.user_id,
                'user_name': message.user.username,
                'command': 'saved_message',
                'message': message.content,
            }))

    # websocket 연결 종료 시 실행 
    def disconnect(self, close_code):
        # 그룹에서 Leave
        async_to_sync(self.channel_layer.group_discard)(
            self.room_channel_layer_group,
            self.channel_name
        )

    # WebSocket 에게 메세지 receive
    # 클라이언트로부터 메세지를 받을 시 실행
    def receive(self, text_data):
        # 메시지를 전달받아서 뿌려줌
        User = get_user_model()

        logger = logging.getLogger(__name__)
        logger.error(text_data)

        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_channel_layer_group = self.room_id

        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user_id = text_data_json['user_id']
        user_name = text_data_json['user_name']
        
        # 클라이언트로부터 받은 메세지를 다시 클라이언트로 보내준다.
        logger.error("mesaage: " + message)

        # Redis-server가 돌고 있는 상태에서 모델을 안만들었더라도 메시지는 왔다갔다 한다.
        # 하지만 DB에 저장되지 않는다. 따라서 models.py의 메시지 모델에 데이터를 삽입해주어야 한다.
        message_object = Message.objects.create(
            # 외래키로 저장할때
            user=User(pk=user_id),
            # 일반필드로 저장할때
            content=message,
            room=Room(pk=self.room_id)
        )

        async_to_sync(self.channel_layer.group_send)(
            self.room_channel_layer_group, 
            {
                'type': 'chat_message', # chat_message를 실행 하고 message, user_name, user_id를 파라미터로 던진다 
                'message': message,
                'user_name': user_name,
                'user_id': user_id,
            }
        )

    def chat_message(self, event):
        message = event['message']
        user_name = event['user_name']
        user_id = event['user_id']

        # WebSocket으로 연결되있는 모든 사용자들에게 메세지 전송
        self.send(text_data=json.dumps({
            'command': 'new_message',
            'message': message,
            'user_name': user_name,
            'user_id': user_id,
        }))

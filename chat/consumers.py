import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from .forms import *
from manager.models import Hikka


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        self.user = self.scope['user']

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        await self.create_message(message)
        await self.channel_layer.group_send(
            self.room_group_name, {
                'type': 'chat_message',
                'message': message
            }
        )

    def get_room(self):
        return Room.objects.get(name=self.room_name)

    @database_sync_to_async
    def get_user(self):
        return Hikka.objects.get(user=self.scope['user'].id)

    @database_sync_to_async
    def create_message(self, text):
        print(type(self.user))
        print(type(self.get_room()))
        former = Message(message_author=self.user, message_room=self.get_room(), message_text=text)
        # former.message_room = self.get_room_instance(self.room_name)
        # former.message_author = self.get_user_instance()
        former.save()

    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))

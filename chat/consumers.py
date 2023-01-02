from .forms import SendMessage
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import *
from .extra_logic import message_validator
from django.contrib.auth.models import AnonymousUser
from manager.models import Hikka


class ChatConsumer(AsyncWebsocketConsumer):

    @database_sync_to_async
    def is_room_empty(self):
        pool = Pool.objects.filter(room_name=self.get_room()).count()
        if pool > 0:
            return True
        else:
            return False

    @database_sync_to_async
    def delete_room(self):
        return Room.objects.get(name=self.get_room()).delete()

    def get_room(self):
        return Room.objects.get(name=self.room_id)

    def get_user(self):
        try:
            return Hikka.objects.get(user=self.scope['user'])
        except Exception as e:
            return 'AnonymousUser'

    @database_sync_to_async
    def create_message(self, text):
        former = Message(message_author=self.user, message_room=self.get_room(), message_text=text)
        former.save()

    @database_sync_to_async
    def add_user_to_room_pool(self):
        check = Pool.objects.filter(username=self.get_user(), room_name_id=self.get_room())
        if check.count():
            pass
        else:
            former = Pool(username=self.get_user(), room_name=self.get_room())
            former.save()

    @database_sync_to_async
    def remove_user_from_room_pool(self):
        former = Pool.objects.filter(username=self.user, room_name=self.get_room())
        former.delete()

    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_id
        self.user = self.scope['user']
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.add_user_to_room_pool()
        await self.accept()

    async def disconnect(self, close_code):
        # await self.remove_user_from_room_pool()
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
                'message': message,
            }
        )

    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message_validator(message)
        }))

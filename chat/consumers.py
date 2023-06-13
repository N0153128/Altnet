import chat.models
from .forms import SendMessage
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import *
from .extra_logic import message_validator
from django.contrib.auth.models import AnonymousUser
from manager.models import Hikka
from chat.views import make_chat_copy
from datetime import datetime
from scripts.archive import make_copy_async, make_copy
import os
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.exceptions import BadRequest
from channels.layers import get_channel_layer


class ChatConsumer(AsyncWebsocketConsumer):

    @database_sync_to_async
    def get_room_async(self):
        return Room.objects.get(id=self.room_id)

    @database_sync_to_async
    def make_async_chat_copy(self):
        now = datetime.now()
        room = Room.objects.get(id=self.room_id)
        messages = Message.objects.filter(message_room=room)
        target = f'{config.COPY_PATH}/room_id_{self.room_id}_copy.txt'
        with open(target, 'a') as f:
            for i in messages.iterator():
                f.write(f'\n{i.message_text} @ {i.pub_date}\n')
        make_copy(config.CHAT_ARCHIVE, f'Chat backup {self.room_id} {now}', [target])
        os.remove(target)

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
        return Room.objects.get(id=self.room_id)

    def get_user(self):
        try:
            return Hikka.objects.get(user=self.scope['user'])
        except Exception:
            return 'AnonymousUser'

    @database_sync_to_async
    def create_message(self, text):
        spl = text.split(':')[0]
        former = Message(message_author=spl, message_room=self.get_room(), message_text=text.strip(f'{spl}:'))
        former.save()

    @database_sync_to_async
    def add_user_to_room_pool(self):
        check = Pool.objects.filter(username=self.get_user(), room_name_id=self.get_room())
        if check.count() > 0:
            check.delete()
            former = Pool(username=self.get_user(), room_name=self.get_room(), channel=self.channel_name)
            former.save()
        else:
            former = Pool(username=self.get_user(), room_name=self.get_room(), channel=self.channel_name)
            former.save()

    @database_sync_to_async
    def add_role(self, username, role):
        if self.get_room().host == self.user:
            check = Role.objects.filter(username=username, role_name=role, room=self.get_room())
            if check.count() > 0:
                check.delete()
                new_role = Role(username=username, role_name=role, room=self.get_room())
                new_role.save()
            else:
                new_role = Role(username=username, role_name=role, room=self.get_room())
                new_role.save()
        else:
            raise BadRequest('Only hosts can do that')

    @database_sync_to_async
    def add_host(self, username):
        if self.get_room().host == self.user:
            check = Host.objects.filter(room=self.get_room(), username=username)
            if check.count() > 0:
                raise BadRequest('This user is already a host')
            else:
                new_host = Host(room=self.get_room(), username=username, responsible=self.user)
                new_host.save()
        else:
            raise BadRequest('Only hosts can do that')


    @database_sync_to_async
    def remove_user_from_room_pool(self):
        former = Pool.objects.filter(username=self.user, room_name=self.get_room())
        former.delete()

    @database_sync_to_async
    def toggle_visibility(self):
        if self.get_room().host == self.user:
            if not self.get_room().is_hidden:
                room = Room.objects.get(id=self.room_id)
                room.is_hidden = True
                room.save()
            elif self.get_room().is_hidden:
                room = Room.objects.get(id=self.room_id)
                room.is_hidden = False
                room.save()
            else:
                raise BadRequest('Something went wrong')
        else:
            raise BadRequest('Only hosts can do that')

    @database_sync_to_async
    def toggle_autoplay(self):
        if self.get_room().host == self.user:
            if not self.get_room().is_autoplay:
                room = Room.objects.get(id=self.room_id)
                room.is_autoplay = True
                room.save()
            elif self.get_room().is_autoplay:
                room = Room.objects.get(id=self.room_id)
                room.is_autoplay = False
                room.save()
            else:
                raise BadRequest('Something went wrong')
        else:
            raise BadRequest('Only hosts can do that')

    @database_sync_to_async
    def toggle_tolerance(self):
        if self.get_room().host == self.user:
            if not self.get_room().is_media_tolerant:
                room = Room.objects.get(id=self.room_id)
                room.is_media_tolerant = True
                room.save()
            elif self.get_room().is_media_tolerant:
                room = Room.objects.get(id=self.room_id)
                room.is_media_tolerant = False
                room.save()
            else:
                raise BadRequest('Something went wrong')
        else:
            raise BadRequest('Only hosts can do that')

    @database_sync_to_async
    def change_room_name(self, data):
        room = Room.objects.get(id=self.room_id)
        if room.host == self.user:
            room.name = data
            room.save()
        else:
            raise BadRequest('Only hosts can do that')

    @database_sync_to_async
    def change_room_description(self, data):
        room = Room.objects.get(id=self.room_id)
        if room.host == self.user:
            room.description = data
            room.save()
        else:
            raise BadRequest('Only hosts can do that')

    @database_sync_to_async
    def remove_all_messages(self):
        if self.get_room().host == self.user:
            messages = Message.objects.filter(message_room=self.get_room())
            messages.delete()

    @database_sync_to_async
    def kick_user(self, username):
        if self.get_room().host == self.user:
            check = Pool.objects.get(room_name=self.get_room().id, username=message_validator(username))
            if check:
                check.delete()
            else:
                raise BadRequest('User not found')
        else:
            raise BadRequest('Only hosts can do that')

    async def kick_channel(self, username):
        if self.is_host(username):
            channel_layer = get_channel_layer()
            await channel_layer.group_discard(
                self.room_group_name,
                await self.get_channel_async(username)
            )

    @database_sync_to_async
    def ban_user(self, username):
        if self.get_room().host == self.user:
            check = Pool.objects.get(room_name=self.get_room().id, username=message_validator(username))
            if check:
                check.delete()
                ban = Ban(username=username, room=self.get_room())
                ban.save()
            else:
                raise BadRequest('User not found')
        else:
            raise BadRequest('Only hosts can do that')

    @database_sync_to_async
    def is_host(self, username):
        if Room.objects.get(id=self.room_id).host == username:
            return True
        else:
            return False

    @database_sync_to_async
    def add_channel(self):
        try:
            check = self.get_channel(self.user, self.get_room())
            if check:
                if check.channel != self.channel_name:
                    check.channel = self.channel_name
                    check.save()

        except Exception:
            new_pair = Pool(username=self.user, room_name=self.get_room(), channel=self.channel_name)
            new_pair.save()

    def get_channel(self, username, room):
        return Pool.objects.get(username=username, room_name=room).channel

    @database_sync_to_async
    def get_channel_async(self, username):
        return Pool.objects.get(username=username, room_name=self.get_room()).channel

    @database_sync_to_async
    def remove_channel(self, username):
        try:
            check = Pool.objects.get(username=username, room_name=self.get_room())
            if check:
                check.delete()
        except Exception:
            raise BadRequest('Channel pair doesn\'t exist')

    async def send_system_msg(self, message):
        await self.send(text_data=json.dumps({
            'message': f'{message}'
        }))

    async def send_private_msg(self, message, recipient):
        channel_layer = get_channel_layer()
        await channel_layer.send(await self.get_channel_async(recipient), {
            "type": "chat.message",
            "message": message,
        })

    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = 'chat_%s' % self.room_id
        self.user = self.scope['user']
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        print(self.channel_name)
        await self.add_user_to_room_pool()
        await self.accept()

    async def disconnect(self, close_code):
        # await self.remove_user_from_room_pool()
        await self.remove_channel(username=self.user)
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print(text_data_json)
        if await self.is_permitted(self.user):
            print('legal')
            if 'message' in text_data_json:
                message = text_data_json['message']
                await self.create_message(message)
                await self.channel_layer.group_send(
                    self.room_group_name, {
                        'type': 'chat_message',
                        'message': message,
                    }
                )
            elif 'action' in text_data_json:
                if text_data_json['action'] == '#test-message':
                    print('LOL KEK AZAZA IT WORKS')
                elif text_data_json['action'] == '#arch':
                    print('copying...')
                    await self.make_async_chat_copy()
                elif text_data_json['action'] == '#erase_messages':
                    await self.remove_all_messages()
                elif text_data_json['action'] == '#toggle_visibility':
                    await self.toggle_visibility()
                elif text_data_json['action'] == '#toggle_autoplay':
                    await self.toggle_autoplay()
                elif text_data_json['action'] == '#toggle_tolerance':
                    await self.toggle_tolerance()
                elif text_data_json['action'] == '#edit_room_name_submit':
                    await self.change_room_name(text_data_json['name'])
                    await self.send_system_msg(message=f'System: room name has been changed to {text_data_json["name"]}')
                elif text_data_json['action'] == '#edit_room_description_submit':
                    await self.change_room_description(text_data_json['name'])
                    await self.send_system_msg(message=f'System: room description has been changed to {text_data_json["name"]}')
                elif text_data_json['action'] == '#username_kick_submit':
                    await self.send_system_msg(message=f'System: {text_data_json["name"]} has been kicked')
                    await self.kick_channel(text_data_json['name'])
                    await self.kick_user(text_data_json['name'])
                elif text_data_json['action'] == '#username_ban_submit':
                    await self.send_system_msg(message=f'System: {text_data_json["name"]} has been banned')
                    await self.kick_channel(text_data_json['name'])
                    await self.ban_user(text_data_json['name'])
                elif text_data_json['action'] == '#role_add_submit':
                    print(f'{text_data_json["username"]} {text_data_json["role_name"]}')
                    await self.add_role(text_data_json['username'], text_data_json['role_name'])
                    await self.send_system_msg(message=f'System: {text_data_json["username"]} got a new role {text_data_json["role_name"]}')
                elif text_data_json['action'] == '#host_add_submit':
                    await self.add_host(text_data_json['name'])
                    await self.send_system_msg(message=f'System: {text_data_json["name"]} is now a host of this room')
        else:
            print('illegal')

    @database_sync_to_async
    def is_permitted(self, username):
        try:
            check = Pool.objects.get(username=username, room_name=self.get_room())
            if check:
                return True
        except chat.models.Pool.DoesNotExist:
            return False

    async def chat_message(self, event):
        if await self.is_permitted(self.user):
            print(await self.is_permitted(self.user))
            message = event['message']
            await self.send(text_data=json.dumps({
                'message': message_validator(message)
           }))
        else:
            pass

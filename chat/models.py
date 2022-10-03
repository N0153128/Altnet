from django.db import models
from manager.models import Hikka
from django.contrib.auth.models import User
import datetime


def user_chat_directory_path(instance, filename):
    now = datetime.datetime.now()
    return f'chat_images/chat_{instance.message_author}_time_{now}_filename_{filename[-5:]}'


class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.TextField(blank=False, null=False, max_length=30)
    description = models.TextField(blank=True, null=True, max_length=200)
    max_slots = models.IntegerField(blank=False, null=False, default=5)
    language_code = models.IntegerField(blank=False, null=False, default=0)
    is_testing = models.BooleanField(blank=False, null=False, default=0)

    def __str__(self):
        return self.name


class Message(models.Model):
    message_author = models.ForeignKey(User, on_delete=models.CASCADE)
    message_room = models.ForeignKey(Room, on_delete=models.CASCADE)
    message_text = models.TextField(blank=False, null=False)
    message_media = models.ImageField(upload_to=user_chat_directory_path, blank=True, null=True)

    def __str__(self):
        return self.message_text


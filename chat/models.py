from django.db import models
from manager.models import Hikka
from django.contrib.auth.models import User
import datetime
import config

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
    pub_date = models.DateTimeField('Date published', auto_now=True)
    is_permanent = models.BooleanField(blank=False, null=False, default=False)

    def __str__(self):
        return self.name


class Message(models.Model):
    message_author = models.CharField('Message author', max_length=150, blank=False, null=False)
    message_room = models.ForeignKey(Room, on_delete=models.CASCADE)
    message_text = models.TextField(blank=False, null=False, max_length=1000)
    message_media = models.ImageField(upload_to=user_chat_directory_path, blank=True, null=True)
    pub_date = models.DateTimeField('Date published', auto_now=True)

    def __str__(self):
        return self.message_text


class Copy(models.Model):
    copy_title = models.CharField('Title of the copy', max_length=150, blank=False, null=False)
    copy_type = models.CharField('Content type', max_length=150, blank=False, null=False)
    copy_path = models.FilePathField('Copy path', path=config.COPY_PATH, match='copy*', max_length=250)
    copy_media = models.FilePathField('Media path', path=config.COPY_MEDIA, match='media*', max_length=250, blank=True)
    downloaded_by_author = models.BooleanField('Was downloaded by author (set to delete)', blank=True, null=True)
    copy_date = models.DateTimeField('Copy creation date', auto_now=True)


class Pool(models.Model):
    username = models.CharField('Username', max_length=150, blank=False, null=False)
    room_name = models.ForeignKey(Room, on_delete=models.CASCADE)
    pub_date = models.DateTimeField('Date published', auto_now=True)


    def __str__(self):
        return str(self.room_name)




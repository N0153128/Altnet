from django.db import models
from django.contrib.auth.models import User
from random import randint
from django.utils import timezone
import datetime


def referral_key():
    composite = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890'
    composite_list = list(composite.strip())
    key = []
    while len(key) < 8:
        key.append(composite_list[randint(0, len(composite_list))])
    return ''.join(key)


class Hikka(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,)
    message = models.CharField('debug message', max_length=100, default='I\'m user!', blank=True, null=True)
    user_pic = models.ImageField(upload_to='avatars', blank=True, null=True)
    language_code = models.IntegerField(default=0)
    is_content_maker = models.BooleanField(default=False, null=True)

    def __str__(self):
        return self.user.username


class Referral(models.Model):

    def is_valid(self):
        # placeholder code V
        now = timezone.now()
        return now - datetime.timedelta(days=7) <= self.created <= now

    value = models.TextField(default=referral_key, blank=False, null=False, max_length=9)
    owner = models.ForeignKey(Hikka, on_delete=models.CASCADE)
    created = models.DateTimeField('Date Created', auto_now=True)

    # def __str__(self):
    #     return self.user.username


class UserPublicPost(models.Model):
    post_author = models.CharField('Message Author', max_length=150, null=False, blank=False)
    post_text = models.CharField('Post text', max_length=250)
    post_date = models.DateTimeField('Post date', auto_now=True)
    language_code = models.IntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return self.post_text


class AdminPublicPost(models.Model):
    post_author = models.ForeignKey(User, on_delete=models.CASCADE)
    post_title = models.CharField('Post title', max_length=100)
    post_text = models.CharField('Post text', max_length=10000)
    post_date = models.DateTimeField('Post date', auto_now=True)
    language_code = models.IntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return self.post_title


class ChangeLog(models.Model):
    note_author = models.ForeignKey(User, on_delete=models.CASCADE)
    note_text = models.CharField('Note text', max_length=300)
    note_date = models.DateTimeField('Note date', auto_now=True)
    language_code = models.IntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return self.note_text

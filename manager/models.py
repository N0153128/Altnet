from django.db import models
from django.contrib.auth.models import User


class Hikka(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,)
    message = models.CharField('debug message', max_length=100, default='I\'m user!', blank=True, null=True)
    user_pic = models.ImageField(upload_to='avatars', blank=True, null=True)
    language_code = models.IntegerField(default=0)

    # def __str__(self):
    #     return self.user.username


class UserPublicPost(models.Model):
    post_author = models.ForeignKey(User, on_delete=models.CASCADE)
    post_text = models.CharField('Post text', max_length=250)
    post_date = models.DateTimeField('Post date', auto_now=True)

    def __str__(self):
        return self.post_text


class AdminPublicPost(models.Model):
    post_author = models.ForeignKey(User, on_delete=models.CASCADE)
    post_title = models.CharField('Post title', max_length=100)
    post_text = models.CharField('Post text', max_length=10000)
    post_date = models.DateTimeField('Post date', auto_now=True)

    def __str__(self):
        return self.post_title


class ChangeLog(models.Model):
    note_author = models.ForeignKey(User, on_delete=models.CASCADE)
    note_text = models.CharField('Note text', max_length=300)
    note_date = models.DateTimeField('Note date', auto_now=True)

    def __str__(self):
        return self.note_text

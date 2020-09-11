from django.db import models
from django.contrib.auth.models import User


class Hikka(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    message = models.CharField('debug message', max_length=100, default='I\'m user!')

    def __str__(self):
        return self.user.username


class UserPublicPost(models.Model):
    post_author = models.CharField('Post author', max_length=30)
    post_text = models.CharField('Post text', max_length=250)
    post_date = models.DateTimeField('Post date', auto_now=True)

    def __str__(self):
        return self.post_text

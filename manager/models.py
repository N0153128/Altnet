from django.db import models
from django.contrib.auth.models import User


class Hikka(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    message = models.CharField('debug message', max_length=100, default='I\'m user!')

    def __str__(self):
        return self.user.username

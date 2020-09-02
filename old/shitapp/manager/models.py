from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils import timezone

class User(models.Model):
    def __str__(self):
        return self.users
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=10000)
    reg_date = datetime
# Create your models here.

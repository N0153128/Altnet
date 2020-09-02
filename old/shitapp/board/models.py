from django.db import models
import datetime
from django.utils import timezone

class Thread(models.Model):
    def __str__(self):
        return self.thread_text
    def was_published(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    thread_title = models.CharField(max_length=100)
    thread_text = models.CharField(max_length=5000)
    pub_date = models.DateTimeField('date published')
    category = models.CharField(max_length=50)
    thread_author = models.CharField(max_length=200)

class Comment(models.Model):
    def __str__(self):
        return self.comment_text
    def was_published(self):
        return self.pub_date >= timezone.now()  - datetime.timedelta(days=1)
    comment_text = models.CharField(max_length=2500)
    comment_post = models.ForeignKey(Thread, on_delete=models.CASCADE)
    comment_author = models.CharField(max_length=200)

# Create your models here.

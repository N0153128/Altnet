from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import User

users = len(User.objects.all())


class Thread(models.Model):

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    thread_title = models.CharField('Thread title', max_length=100)
    thread_text = models.TextField('Thread text', max_length=10000)
    pub_date = models.DateTimeField('Date published', auto_now=True)
    CATEGORY_CHOICES = [('Random', 'Random'), ('Broadcast', 'Broadcast'), ('Animation', 'Animation'), ('Artwork', 'Artwork'), ('Cinematics', 'Cinematics'), ('Videogames', 'Videogames')]
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    thread_author = models.ForeignKey(User, on_delete=models.CASCADE)
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

    def __str__(self):
        return self.thread_title


class Comment(models.Model):
    def __str__(self):
        return self.comment_text

    def was_published(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    comment_text = models.TextField('Comment text', max_length=10000)
    comment_post = models.ForeignKey(Thread,  on_delete=models.CASCADE)
    comment_author = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField('Date published', null=True, blank=True, auto_now=True)

# Create your models here.

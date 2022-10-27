from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import User


users = len(User.objects.all())


def user_thread_directory_path(instance, filename):
    now = datetime.datetime.now()
    return f'thread_images/thread_{instance.thread_author}_time_{now}_filename_{filename[-5:]}'


def user_comment_directory_path(instance, filename):
    now = datetime.datetime.now()
    return f'comment_images/comment_{instance.comment_author}_time_{now}_filename_{filename[-5:]}'


class Thread(models.Model):

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    thread_title = models.CharField('Thread title', max_length=100)
    thread_text = models.TextField('Thread text', max_length=10000)
    pub_date = models.DateTimeField('Date published', auto_now=True)
    CATEGORY_CHOICES = [('Random', 'Random'), ('Broadcast', 'Broadcast'), ('Animation', 'Animation'), ('Artwork', 'Artwork'), ('Cinematics', 'Cinematics'), ('Videogames', 'Videogames')]
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    thread_author = models.CharField('Thread Author', max_length=150, blank=False, null=False)
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'
    thread_pic = models.ImageField(upload_to=user_thread_directory_path, blank=True, null=True)
    language_code = models.IntegerField(blank=True, null=True, default=0)

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
    comment_author = models.CharField('Comment Author', blank=False, null=False, max_length=150)
    pub_date = models.DateTimeField('Date published', null=True, blank=True, auto_now=True)
    comment_pic = models.ImageField(upload_to=user_comment_directory_path, blank=True, null=True)

# Create your models here.

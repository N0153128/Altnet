from django.db import models
import datetime
from django.utils import timezone


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
    thread_author = models.CharField('Thread Author', max_length=150, blank=False, null=False)
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'
    thread_pic = models.ImageField(upload_to=user_thread_directory_path, blank=True, null=True)
    language_code = models.IntegerField(blank=True, null=True, default=0)
    visible = models.BooleanField(blank=False, null=False, default=True)

    def __str__(self):
        return self.thread_title


class Category(models.Model):

    CATEGORY_CHOICES = [('Random', 'Random'), ('Broadcast', 'Broadcast'), ('Animation', 'Animation'),
                        ('Artwork', 'Artwork'), ('Cinematics', 'Cinematics'), ('Videogames', 'Videogames'),
                        ('Writing', 'Writing'), ('Fresh Air', 'Fresh Air'), ('Esports', 'Esports'),
                        ('Politics', 'Politics'), ('Feedback', 'Feedback'), ('HiTech', 'HiTech'),
                        ('Offline', 'Offline'), ('Online', 'Online'), ('Memes', 'Memes'),
                        ('NSFW', 'NSFW'), ('Custom', 'Custom')]
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, default='Random')
    visible = models.BooleanField(default=True, null=False, blank=False)

    def __str__(self):
        return f'{self.category}'


class PairMeta(models.Model):
    cat_thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    cat_name = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.cat_name}: {self.cat_thread}'


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
    visible = models.BooleanField(blank=False, null=False, default=True)

# Create your models here.

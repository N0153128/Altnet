from django.db import models
import datetime
from django.utils import timezone
import board.forms as model_forms
from .views import anonymous_validator
from django.http import Http404
from hikka.settings import MEDIA_ROOT
from manager.models import *


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

    @staticmethod
    def fetch_latest_threads(loc_option, cat=None):
        if cat is not None:
            latest_threads = Thread.objects.filter(language_code=loc_option, visible=True,
                                                   pairmeta__cat_name=cat).order_by('-pub_date')[:10]
        else:
            latest_threads = Thread.objects.filter(language_code=loc_option, visible=True).order_by('-pub_date')[:10]
        thread_list = {}
        for item in latest_threads.iterator():
            load = {'id': item.id, 'thread_title': item.thread_title, 'thread_text': item.thread_text,
                    'pub_date': item.pub_date, 'category': str(PairMeta.objects.get(cat_thread=item).cat_name),
                    'thread_author': item.thread_author, 'thread_pic': item.thread_pic, 'comments': []}
            comments = Comment.objects.filter(comment_post=item, visible=True)
            for i in comments:
                comment = {'id': i.id, 'comment_text': i.comment_text, 'comment_author': i.comment_author,
                           'pub_date': i.pub_date, 'comment_pic': i.comment_pic, 'visible': i.visible}
                load['comments'].append(comment)

            thread_list[item.thread_title] = load
        return thread_list

    @staticmethod
    def create_thread(request):
        form = model_forms.ThreadForm(request.POST, request.FILES)
        if form.is_valid():
            former = form.save(commit=False)
            former.category = form.cleaned_data['category']
            print(former.category)
            if former.category == 'Broadcast':
                if request.user.is_staff:
                    former.thread_author = request.user
                else:
                    raise IllegalAction('suka')
            else:
                if request.user.is_authenticated:
                    former.thread_author = request.user
                    former.language_code = Hikka.objects.get(user=request.user.id).language_code
                else:
                    former.thread_author = anonymous_validator(request)
                    former.language_code = 0
                if request.FILES:
                    former.thread_pic = request.FILES['thread_pic']
                former.save()
                n_cat = Category.objects.get(category=former.category)
                category = PairMeta(cat_name=n_cat, cat_thread=former)
                category.save()
        else:
            raise Http404(form.errors)

    def handle_uploaded_thread_image(f, name):
        now = datetime.datetime.now()
        with open(f'{MEDIA_ROOT}/thread_images/{name}-{now}-{f.name[-5:]}', 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)

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

    @staticmethod
    def fetch_latest_comments(loc_option):
        latest_comments = Comment.objects.filter(comment_post__language_code=loc_option, visible=True).order_by(
            '-pub_date')[:5]
        return latest_comments

    def create_comment(request, pk=None):
        form = model_forms.CommentForm(request.POST, request.FILES)
        if form.is_valid():
            former = form.save(commit=False)
            if pk is not None:
                thread = Thread.objects.get(id=pk)
            else:
                thread = Thread.objects.get(id=form.cleaned_data['key'])

            former.comment_text = form.cleaned_data['comment_text']
            if request.user.is_authenticated:
                former.comment_author = request.user
            else:
                former.comment_author = anonymous_validator(request)
            former.comment_post = thread
            if request.FILES:
                former.comment_pic = request.FILES['comment_pic']
            former.save()
        else:
            raise Http404("Something went wrong")

    def handle_uploaded_comment_image(f, name):
        with open(f'{MEDIA_ROOT}/comment_images/{name}-{f.name[:-5]}', 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)

# Create your models here.

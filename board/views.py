from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import loader
from .models import *
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import ThreadForm, CommentForm, UserPicUpload
from django.views.generic.edit import DeleteView
from django.shortcuts import render
from manager.forms import *
from hikka.settings import MEDIA_ROOT
import datetime
from scripts.loc import Errors, UI, Profile, Categories
from random import randint, choices
from scripts.localisation import loc_resolver


def random_name():
    noun = ['Apple', 'Grape', 'Hero', 'Nickel', 'Zinc', 'Rock', 'Paper', 'Joker', 'Beat', 'Aug', 'Runner', 'Miracle']
    adjective = ['Shitty', 'Slippy', 'Explosive', 'Luminous', 'Advanced', 'Creative', 'Burning', 'Sweaty', 'Leet',
                 'Apex', 'Funny', 'Raging']
    tag = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    randomized_tag = choices(tag, k=4)
    return ''.join(adjective[randint(0, len(adjective)-1)]) + '-' + ''.join(noun[randint(0, len(noun)-1)]) + '#' + \
           ''.join(randomized_tag)


def anonymous_validator(request):
    name = random_name()
    if 'Anonymous-Name' in request.session:
        for key, value in request.session.items():
            print('{} => {}'.format(key, value))
        return request.session['Anonymous-Name']
    else:
        request.session['Anonymous-Name'] = name
        for key, value in request.session.items():
            print('{} => {}'.format(key, value))
        return name


def handle_uploaded_thread_image(f, name):
    now = datetime.datetime.now()
    with open(f'{MEDIA_ROOT}/thread_images/{name}-{now}-{f.name[-5:]}', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def handle_uploaded_comment_image(f, name):
    with open(f'{MEDIA_ROOT}/comment_images/{name}-{f.name[:-5]}', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def fetch_latest_threads(loc_option, cat=None):
    if cat is not None:
        latest_threads = Thread.objects.filter(language_code=loc_option, visible=True, pairmeta__cat_name=cat).order_by('-pub_date')[:10]
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


def fetch_latest_comments(loc_option):
    latest_comments = Comment.objects.filter(comment_post__language_code=loc_option, visible=True).order_by('-pub_date')[:5]
    return latest_comments


def initial_check(request):
    if request.user.is_authenticated:
        username = request.user.username
        loc_option = Hikka.objects.get(user=request.user.id).language_code

    else:
        username = anonymous_validator(request)
        loc_option = 0
    return username, loc_option


def create_thread(request):
    form = ThreadForm(request.POST, request.FILES)
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


def create_comment(request, pk=None):
    form = CommentForm(request.POST, request.FILES)
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


def create_post(request):
    form = CreateMessage(request.POST)
    if form.is_valid():
        former = form.save(commit=False)
        former.post_text = form.cleaned_data['post_text']
        former.post_author = request.user
        former.language_code = Hikka.objects.get(user=request.user.id).language_code
        former.save()


def update_avatar(request):
    obj = Hikka.objects.get(user=request.user.id)
    form = UserPicUpload(request.POST, request.FILES, instance=obj)
    if form.is_valid():
        form.save()


def board(request):
    username, loc_option = initial_check(request)
    template = loader.get_template('board/board.html')
    cat_list = Category.objects.filter(visible=True)
    if request.method == 'POST':
        if 'thread' in request.POST:
            create_thread(request)
            return HttpResponseRedirect(request.path_info)
        elif 'cmm' in request.POST:
            create_comment(request)
            return HttpResponseRedirect(request.path_info)
    thread_form = ThreadForm()
    comment_form = CommentForm()
    context = {
        'loc': loc_resolver('board'),
        'lang': loc_option,
        'latest_comments': fetch_latest_comments(loc_option),
        'thread_form': thread_form,
        'comment_form': comment_form,
        'username': username,
        'thread_list': fetch_latest_threads(loc_option),
        'category_list': cat_list,
    }
    return HttpResponse(template.render(context, request))


def thread_view(request, pk):
    username, loc_option = initial_check(request)
    thread = Thread.objects.get(id=pk)
    comments = Comment.objects.filter(comment_post=thread, visible=True)
    template = loader.get_template('board/thread.html')
    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            create_comment(request, pk)
            return HttpResponseRedirect(reverse('Board:thread', kwargs={'pk': thread.id}))
        else:
            raise Http404("Something went wrong")
    form = CommentForm()
    context = {
        'loc': loc_resolver('thread'),
        'lang': loc_option,
        'thread': thread,
        'form': form,
        'comments': comments,
        'username': username,
    }
    return HttpResponse(template.render(context, request))

@login_required
def account(request):
    threads = Thread.objects.filter(thread_author=request.user).order_by('-pub_date')
    comments = Comment.objects.filter(comment_author=request.user)
    messages = UserPublicPost.objects.filter(post_author=request.user).order_by('-post_date')
    loc_option = Hikka.objects.get(user=request.user.id).language_code
    try:
        additional = Hikka.objects.get(user__id=request.user.id)
    except Hikka.DoesNotExist:
        additional = None
        hikka = Hikka(user=request.user)
        hikka.save()
        return HttpResponseRedirect(request.path_info)
    form = UserPicUpload

    if request.method == 'POST':
        if 'post' in request.POST:
            create_post(request)
            return HttpResponseRedirect(reverse('Board:user'))
        elif 'upload_user_pic' in request.POST:
            update_avatar(request)
            return HttpResponseRedirect(request.path_info)
    context = {
        'loc': loc_resolver('account'),
        'lang': loc_option,
        'threads': threads,
        'comments': comments,
        'messages': messages,
        'form': CreateMessage,
        'upload': UserPicUpload,
        'add': additional,
        'upl': form,
    }
    return render(request, 'user.html', context)


def guest(request, username):
    profile = Profile
    errors = Errors
    user = User.objects.get(username=username)
    threads = Thread.objects.filter(thread_author=username)
    comments = Comment.objects.filter(comment_author=username)
    messages = UserPublicPost.objects.filter(post_author=username)
    additional = Hikka.objects.get(user__username=username)
    form = UserPicUpload
    loc = UI
    loc_option = Hikka.objects.get(user=request.user.id).language_code
    context = {
        'lang': loc_option,
        'UI': loc,
        'host': user,
        'threads': threads,
        'comments': comments,
        'messages': messages,
        'add': additional,
        'upl': form,
        'profile': profile,
        'errors': errors,
    }
    return render(request, 'guest.html', context)


def category(request, cat):
    username, loc_option = initial_check(request)
    cat = Category.objects.get(category=cat)
    cat_list = Category.objects.filter(visible=True)
    if request.method == 'POST':
        if 'cmm' in request.POST:
            create_comment(request)
            return HttpResponseRedirect(request.path_info)
        elif 'thread' in request.POST:
            create_thread(request)
            return HttpResponseRedirect(request.path_info)
    context = {
        'loc': loc_resolver('category'),
        'lang': loc_option,
        'thread_list': fetch_latest_threads(loc_option, cat),
        'form': ThreadForm,
        'category': cat.category,
        'category_list': cat_list,
    }
    return render(request, 'board/category.html', context)


class ThreadDelete(DeleteView):
    model = Thread
    success_url = reverse_lazy('Board:board')


def message_remove(request, pk):
    topic = UserPublicPost.objects.get(id=pk)
    if request.user.is_authenticated:
        if request.user.username == topic.post_author:
            topic.delete()
            return HttpResponseRedirect(reverse('Board:user'))
    else:
        if request.session['Anonymous-Name'] == topic.post_author:
            topic.delete()
            return HttpResponseRedirect(reverse('Board:user'))
        else:
            raise Http404('dafak')


def thread_remove(request, pk):
    # can potentially break the webpage, as it doesnt remove the PairMeta record, causing the Board page to throw
    # an error. requires further research.
    topic = Thread.objects.get(id=pk)
    if request.user.is_authenticated:
        if request.user.username == topic.thread_author:
            topic.delete()
            return HttpResponseRedirect(reverse('Board:board'))
    else:
        if request.session['Anonymous-Name'] == topic.thread_author:
            topic.delete()
            return HttpResponseRedirect(reverse('Board:board'))
        else:
            raise Http404('dafak')


def comment_remove(request, pk, tpk):
    topic = Comment.objects.get(id=pk)
    if request.user.is_authenticated:
        if request.user.username == topic.comment_author:
            topic.delete()
            return HttpResponseRedirect(reverse('Board:thread', kwargs={'pk': tpk}))
    else:
        if request.session['Anonymous-Name'] == topic.comment_author:
            topic.delete()
            return HttpResponseRedirect(reverse('Board:thread', kwargs={'pk': tpk}))
        else:
            raise Http404('dafak')


class MessageDelete(DeleteView):
    model = UserPublicPost
    success_url = reverse_lazy('Board:user')


class CommentDelete(DeleteView):
    model = Comment

    def get_success_url(self):
        return reverse('Board:thread', kwargs={'pk': self.object.comment_post.id})

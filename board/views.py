from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import loader
from .models import Thread, Comment
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import ThreadForm, CommentForm, UserPicUpload, ThreadPicUpload
from django.views.generic.edit import DeleteView
from django.shortcuts import render
from manager.forms import *
from hikka.settings import MEDIA_ROOT
import datetime
import os
from loc import UI, Errors, Headers, Board, Categories
from loc.content import Thread as locThread


def handle_uploaded_thread_image(f, name):
    now = datetime.datetime.now()
    with open(f'{MEDIA_ROOT}/thread_images/{name}-{now}-{f.name[-5:]}', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def handle_uploaded_comment_image(f, name):
    with open(f'{MEDIA_ROOT}/comment_images/{name}-{f.name[:-5]}', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


@login_required
def board(request):
    language_key = Hikka.objects.get(user=request.user.id).language_code
    latest_threads = Thread.objects.filter(language_code=language_key).order_by('-pub_date')[:10]
    template = loader.get_template('board/board.html')
    latest_comments = Comment.objects.filter(comment_post__language_code=language_key).order_by('-pub_date')[:10]
    loc = UI
    if request.user.is_authenticated:
        loc_option = Hikka.objects.get(user=request.user.id).language_code
    else:
        loc_option = 0
    headers = Headers
    errors = Errors
    board_ = Board
    thread = locThread
    categories = Categories
    if request.method == 'POST':
        if 'cmm' in request.POST:
            form = CommentForm(request.POST, request.FILES)
            if form.is_valid():
                former = form.save(commit=False)
                former.comment_text = form.cleaned_data['comment_text']
                former.comment_author = request.user
                thread = Thread.objects.get(id=form.cleaned_data['key'])
                former.comment_post = thread
                if request.FILES:
                    former.comment_pic = request.FILES['comment_pic']
                    # handle_uploaded_comment_image(request.FILES['comment_pic'], request.user.username)
                former.save()
                return HttpResponseRedirect(request.path_info)
            else:
                raise Http404("Something went wrong")

        elif 'thread' in request.POST:
            form = ThreadForm(request.POST, request.FILES)
            if form.is_valid():
                former = form.save(commit=False)
                former.category = form.cleaned_data['category']
                if former.category == 'Broadcast':
                    if request.user.is_staff:
                        former.thread_author = request.user
                    else:
                        raise IllegalAction('suka')
                former.thread_author = request.user
                former.language_code = Hikka.objects.get(user=request.user.id).language_code
                if request.FILES:
                    former.thread_pic = request.FILES['thread_pic']
                    # handle_uploaded_thread_image(request.FILES['thread_pic'], request.user.username)
                former.save()
                # os.remove(f'{MEDIA_ROOT}/{request.FILES["thread_pic"].name}')
                return HttpResponseRedirect(request.path_info)
            else:
                raise Http404(form.errors)
    thread_form = ThreadForm()
    comment_form = CommentForm()
    context = {
        'UI': loc,
        'headers': headers,
        'errors': errors,
        'lang': loc_option,
        'board': board_,
        'locThread': thread,
        'categories': categories,
        'latest_threads': latest_threads,
        'latest_comments': latest_comments,
        'thread_form': thread_form,
        'comment_form': comment_form,
    }
    return HttpResponse(template.render(context, request))


@login_required
def thread_view(request, pk):
    thread = Thread.objects.get(id=pk)
    comments = Comment.objects.filter(comment_post=thread)
    template = loader.get_template('board/thread.html')
    loc = UI
    if request.user.is_authenticated:
        loc_option = Hikka.objects.get(user=request.user.id).language_code
    else:
        loc_option = 0
    headers = Headers
    errors = Errors
    board_ = Board
    locthread = locThread
    categories = Categories
    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            former = form.save(commit=False)
            former.comment_text = form.cleaned_data['comment_text']
            former.comment_author = request.user
            former.comment_post = thread
            if request.FILES:
                former.comment_pic = request.FILES['comment_pic']
            former.save()
            return HttpResponseRedirect(reverse('Board:thread', kwargs={'pk': thread.id}))
        else:
            raise Http404("Something went wrong")
    form = CommentForm()
    context = {
        'lang': loc_option,
        'UI': loc,
        'headers': headers,
        'errors': errors,
        'board': board_,
        'locThread': locthread,
        'categories': categories,
        'thread': thread,
        'form': form,
        'comments': comments
    }
    return HttpResponse(template.render(context, request))


@method_decorator(login_required, name='dispatch')
class CommentsView(generic.DetailView):
    model = Comment
    template_name = 'board/comments.html'


@method_decorator(login_required, name='dispatch')
class CommentView(generic.DetailView):
    model = Thread
    template_name = 'board/comment.html'


class ThreadDelete(DeleteView):
    model = Thread
    success_url = reverse_lazy('Board:board')


def message_remove(request, pk):
    topic = UserPublicPost.objects.get(id=pk)
    if request.user.id == topic.post_author.id:
        topic.delete()
        return HttpResponseRedirect(reverse('Board:user'))
    else:
        raise Http404('Illegal request')


def thread_remove(request, pk):
    topic = Thread.objects.get(id=pk)
    if request.user.id == topic.thread_author.id:
        topic.delete()
        return HttpResponseRedirect(reverse('Board:board'))
    else:
        raise Http404('Illegal request')


def comment_remove(request, pk):
    topic = Comment.objects.get(id=pk)
    if request.user.id == topic.comment_author.id:
        topic.delete()
        return HttpResponseRedirect(reverse('Board:thread', kwargs={'pk': topic.comment_post.id}))
    else:
        raise Http404('Illegal request')


class MessageDelete(DeleteView):
    model = UserPublicPost
    success_url = reverse_lazy('Board:user')


class CommentDelete(DeleteView):
    model = Comment

    def get_success_url(self):
        return reverse('Board:thread', kwargs={'pk': self.object.comment_post.id})


@login_required
def account(request):
    threads = Thread.objects.filter(thread_author=request.user)
    comments = Comment.objects.filter(comment_author=request.user)
    messages = UserPublicPost.objects.filter(post_author=request.user)
    loc = UI
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
            form = CreateMessage(request.POST)
            if form.is_valid():
                former = form.save(commit=False)
                former.post_text = form.cleaned_data['post_text']
                former.post_author = request.user
                former.language_code = Hikka.objects.get(user=request.user.id).language_code
                former.save()
                return HttpResponseRedirect(reverse('Board:user'))
        elif 'upload_user_pic' in request.POST:
            obj = Hikka.objects.get(user=request.user.id)
            form = UserPicUpload(request.POST, request.FILES, instance=obj)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(request.path_info)
    context = {
        'lang': loc_option,
        'UI': loc,
        'threads': threads,
        'comments': comments,
        'messages': messages,
        'form': CreateMessage,
        'upload': UserPicUpload,
        'add': additional,
        'upl': form
    }
    return render(request, 'user.html', context)


@login_required
def guest(request, username):
    user = User.objects.get(username=username)
    threads = Thread.objects.filter(thread_author__username=username)
    comments = Comment.objects.filter(comment_author__username=username)
    messages = UserPublicPost.objects.filter(post_author__username=username)
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
        'upl': form
    }
    return render(request, 'guest.html', context)


@login_required
def category(request, cat):
    thread_list = Thread.objects.filter(category=cat).order_by('-pub_date')
    comments_list = Comment.objects.filter(comment_post__category=cat)
    loc = UI
    loc_option = Hikka.objects.get(user=request.user.id).language_code
    if request.method == 'POST':
        if 'cmm' in request.POST:
            form = CommentForm(request.POST)
            if form.is_valid():
                former = form.save(commit=False)
                former.comment_text = form.cleaned_data['comment_text']
                former.comment_author = request.user
                thread = Thread.objects.get(id=form.cleaned_data['key'])
                former.comment_post = thread
                former.save()
                return HttpResponseRedirect(request.path_info)
            else:
                raise Http404("Something went wrong")

        elif 'thread' in request.POST:
            form = ThreadForm(request.POST)
            if form.is_valid():
                former = form.save(commit=False)
                former.category = form.cleaned_data['category']
                former.thread_author = request.user
                former.save()
                return HttpResponseRedirect(request.path_info)
            else:
                raise Http404(form.errors)
    context = {
        'lang': loc_option,
        'UI': loc,
        'latest_threads': thread_list,
        'latest_comments': comments_list,
        'form': ThreadForm,
        'category': cat
    }
    return render(request, 'board/category.html', context)



from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import loader
from .models import Thread, Comment
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import ThreadForm, CommentForm
from django.views.generic.edit import DeleteView
from django.shortcuts import render
from django.contrib.auth.models import User


@login_required
def board(request):
    # thread = get_object_or_404(Thread)
    latest_threads = Thread.objects.order_by('-pub_date')[:10]
    template = loader.get_template('board/board.html')
    latest_comments = Comment.objects.order_by('-pub_date')[:10]

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
                return HttpResponseRedirect(reverse('Board:board'))
            else:
                raise Http404("Something went wrong")

        elif 'thread' in request.POST:
            form = ThreadForm(request.POST)
            if form.is_valid():
                former = form.save(commit=False)
                former.category = form.cleaned_data['category']
                former.thread_author = request.user
                former.save()
                return HttpResponseRedirect(reverse('Board:board'))
            else:
                raise Http404("Something went wrong")
    form = ThreadForm()
    context = {
        'latest_threads': latest_threads,
        'latest_comments': latest_comments,
        'form': form,
    }
    return HttpResponse(template.render(context, request))


@login_required
def thread_view(request, pk):
        thread = Thread.objects.get(id=pk)
        comments = Comment.objects.filter(comment_post = thread)
        template = loader.get_template('board/thread.html')

        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                former = form.save(commit=False)
                former.comment_text = form.cleaned_data['comment_text']
                former.comment_author = request.user
                former.comment_post = thread
                former.save()
                return HttpResponseRedirect(reverse('Board:thread', kwargs={'pk':thread.id}))
            else:
                raise Http404("Something went wrong")
        form = CommentForm()
        context = {
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


class CommentDelete(DeleteView):
    model = Comment

    def get_success_url(self):
        return reverse('Board:thread', kwargs={'pk': self.object.comment_post.id})


@login_required
def account(request):
    return render(request, 'user.html')


@login_required
def guest(request, username):
    user = User.objects.get(username=username)
    context = {
        'host': user
    }
    return render(request, 'guest.html', context)
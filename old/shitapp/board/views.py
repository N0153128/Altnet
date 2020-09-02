# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from .models import Thread, Comment
from django.urls import reverse
from django.db.models import F
from django.views import generic

class IndexView(generic.ListView):
    template_name = 'board/board.html'
    context_object_name = 'threads_list'
    def get_queryset(self):
        """Return the last ten published"""
        return Thread.objects.order_by('-pub_date')[:10]


class ThreadView(generic.DetailView):
    model = Thread
    template_name = 'board/thread.html'

class CommentView(generic.DetailView):
    model = Thread
    template_name = 'board/comment.html'

class CommentsView(generic.DetailView):
    model = Comment
    template_name = 'board/comments.html'
from django.shortcuts import render
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render
from board.models import *
from .models import *


@method_decorator(login_required, name='dispatch')
class authsh(generic.View):
    template_name = 'registration/blank.html'


@login_required
def meview(request):
    latest_threads = Thread.objects.order_by('-pub_date')[:10]
    latest_posts = UserPublicPost.objects.order_by('-post_date')[:10]
    admin_posts = AdminPublicPost.objects.order_by('-post_date')[:10]
    context = {
        'threads': latest_threads,
        'posts': latest_posts,
        'admins': admin_posts
    }
    return render(request, 'me.html', context)

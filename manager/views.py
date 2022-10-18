from django.shortcuts import render
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render
from board.models import *
from .models import *
from loc import UI, Headers, Errors, Me
from board.templatetags import loc_extra


@method_decorator(login_required, name='dispatch')
class authsh(generic.View):
    template_name = 'registration/blank.html'


def meview(request):
    if request.user.is_authenticated:
        loc_option = Hikka.objects.get(user=request.user.id).language_code
    else:
        loc_option = 0
    latest_threads = Thread.objects.filter(language_code=loc_option).order_by('-pub_date')[:10]
    latest_posts = UserPublicPost.objects.filter(language_code=loc_option).order_by('-post_date')[:10]
    admin_posts = AdminPublicPost.objects.filter(language_code=loc_option).order_by('-post_date')[:10]
    loc = UI
    headers = Headers
    errors = Errors
    me = Me
    context = {
        'me': me,
        'headers': headers,
        'errors': errors,
        'lang': loc_option,
        'UI': loc,
        'threads': latest_threads,
        'posts': latest_posts,
        'admins': admin_posts
    }
    return render(request, 'me.html', context)

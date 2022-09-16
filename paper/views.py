from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from manager.models import ChangeLog
from loc import UI, Info
from manager.models import Hikka


@method_decorator(login_required, name='dispatch')
class InfoView(generic.TemplateView):
    template_name = 'info.html'


def info_view(request):
    logs = ChangeLog.objects.order_by('-note_date')[:10]
    loc = UI
    if request.user.is_authenticated:
        loc_option = Hikka.objects.get(user=request.user.id).language_code
    else:
        loc_option = 0
    info = Info
    context = {
        'info': info,
        'UI': loc,
        'lang': loc_option,
        'logs': logs,
    }
    return render(request, 'info.html', context)


def index(request):
    if request.user.is_authenticated:
        return redirect(reverse('Manager:me'))
    else:
        return render(request, 'index.html')

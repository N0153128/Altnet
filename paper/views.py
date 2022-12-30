from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from manager.models import ChangeLog
from manager.models import Hikka
from scripts.loc import Info, UI
from scripts.localisation import loc_resolver


@method_decorator(login_required, name='dispatch')
class InfoView(generic.TemplateView):
    template_name = 'info.html'


def info_view(request):
    if request.user.is_authenticated:
        loc_option = Hikka.objects.get(user=request.user.id).language_code
    else:
        loc_option = 0
    logs = ChangeLog.objects.filter(language_code=loc_option).order_by('-note_date')[:10]
    context = {
        'loc': loc_resolver('info'),
        'lang': loc_option,
        'logs': logs,
    }
    return render(request, 'info.html', context)


def index(request):
    if request.user.is_authenticated:
        return redirect(reverse('Manager:me'))
    else:
        return render(request, 'index.html')

from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from manager.models import ChangeLog


@method_decorator(login_required, name='dispatch')
class InfoView(generic.TemplateView):
    template_name = 'info.html'


def info_view(request):
    logs = ChangeLog.objects.order_by('-note_date')[:10]
    context = {
        'logs': logs,
    }
    return render(request, 'info.html', context)


def index(request):
    if request.user.is_authenticated:
        return redirect(reverse('Manager:me'))
    else:
        return render(request, 'index.html')

from django.shortcuts import render
from django.views.generic import TemplateView
from django.shortcuts import render
from .models import Archive
from django.http import HttpResponse
from django.template import loader


def paperhome(request):
    papers = Archive.objects.all()
    template = loader.get_template('archive/index.html')
    context = {
        'papers': papers
    }
    return HttpResponse(template.render(context, request))

from django.shortcuts import render
from django.contrib.auth import forms
from django.contrib.auth import authenticate, login
from django.views.generic import TemplateView

#class HomePageView(TemplateView):
   # template_name = home.html

def index(request):
    return render(request, 'index.html')
def account(request):
    return render(request, 'registration/user.html')
def authsh(request):
    return render(request, 'registration/blank.html')
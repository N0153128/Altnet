from django.urls import path, include
from .views import *


app_name = 'Archive'
urlpatterns = [
    path('', paperhome, name='index'),
]

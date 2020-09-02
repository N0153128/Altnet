from django.urls import path, include
from . import views

app_name = 'Paper'
urlpatterns = [
    path('', views.index, name='index'),
    path('info/', views.InfoView.as_view(), name='info'),
]
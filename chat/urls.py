from django.urls import path
from . import views


app_name = 'Chat'
urlpatterns = [
    path('', views.index, name='chat'),
    path('<str:room_name>/', views.room, name='room'),

]
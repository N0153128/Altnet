from django.shortcuts import render
from django.template import loader


def index(request):
    return render(request, 'chat.html')


def room(request, room_name):
    return render(request, 'room.html', {
        'room_name': room_name,
    })

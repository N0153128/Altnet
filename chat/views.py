from django.shortcuts import render, loader
from loc import UI, Errors, Headers, Board, Categories, Chat
from loc.content import Thread as locThread
from manager.models import Hikka
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .models import *
from .forms import *


def index(request):
    loc = UI
    headers = Headers
    errors = Errors
    board_ = Board
    thread = locThread
    template = loader.get_template('chat.html')
    categories = Categories
    chat = Chat
    if request.user.is_authenticated:
        loc_option = Hikka.objects.get(user=request.user.id).language_code
    else:
        loc_option = 0
    room_list = Room.objects.filter(language_code=loc_option)
    pool = {}
    for item in room_list.iterator():
        load = []
        instance = item.pool_set.all()
        for i in instance:
            load.append(i.username)
        pool[item.name] = load
    context = {
        'UI': loc,
        'headers': headers,
        'errors': errors,
        'lang': loc_option,
        'board': board_,
        'locThread': thread,
        'categories': categories,
        'room_list': room_list,
        'chat': chat,
        'pool': pool,

    }
    return HttpResponse(template.render(context, request))


def room(request, room_name):
    chat_form = SendMessage()
    language_key = Hikka.objects.get(user=request.user.id).language_code
    loc = UI
    headers = Headers
    errors = Errors
    board_ = Board
    thread = locThread
    template = loader.get_template('room.html')
    categories = Categories
    if request.user.is_authenticated:
        loc_option = Hikka.objects.get(user=request.user.id).language_code
    else:
        loc_option = 0
    messages = Message.objects.filter(message_room__name=room_name)
    context = {
        'UI': loc,
        'headers': headers,
        'errors': errors,
        'lang': loc_option,
        'board': board_,
        'locThread': thread,
        'categories': categories,
        'room_name': room_name,
        'messages': messages,
        'chat_form': chat_form,
    }
    return HttpResponse(template.render(context, request))


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
    room_form = CreateRoom()
    for item in room_list.iterator():
        load = {}
        load['id'] = item.id
        load['name'] = item.name
        load['host'] = item.host
        load['description'] = item.description
        load['max_slots'] = item.max_slots
        load['language_code'] = item.language_code
        load['is_testing'] = item.is_testing
        load['users'] = []
        user_pool = item.pool_set.all()
        for i in user_pool:
            load['users'].append(str(i.username))
        pool[item.name] = load
    if request.method == 'POST':
        form = CreateRoom(request.POST)
        if form.is_valid():
            former = form.save(commit=False)
            former.name = form.cleaned_data['name']
            former.description = form.cleaned_data['description']
            former.max_slots = form.cleaned_data['max_slots']
            former.host = request.user
            former.language_code = loc_option
            former.save()
            return HttpResponseRedirect(request.path_info)

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
        'room_form': room_form,

    }
    return HttpResponse(template.render(context, request))


def room(request, room_id):
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
    messages = Message.objects.filter(message_room__id=room_id)
    room_name = Room.objects.get(id=room_id).name
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


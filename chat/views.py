from django.shortcuts import loader

from scripts.loc import Errors, UI, Board, Categories, Headers, Chat, Thread as locThread
from manager.models import Hikka
from django.http import HttpResponse, HttpResponseRedirect
from .forms import *
from board.views import anonymous_validator
from scripts.archive import make_copy
from datetime import datetime
from django.urls import reverse
from scripts.localisation import loc_resolver


def make_chat_copy(room_id, room_name):
    now = datetime.now()
    room = Room.objects.get(id=room_id)
    messages = Message.objects.filter(message_room=room)
    target = f'{config.COPY_PATH}/room_id_2_copy.txt'
    with open(target, 'a') as f:
        for i in messages.iterator():
            f.write(f'\n{i.message_text} @ {i.pub_date}\n')
    make_copy(config.CHAT_ARCHIVE, f'Chat backup {room_name} {now}', [target])


def index(request):
    if request.user.is_authenticated:
        username = request.user.username
        loc_option = Hikka.objects.get(user=request.user.id).language_code
    else:
        username = anonymous_validator(request)
        loc_option = 0
    template = loader.get_template('chat.html')
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
        if len(load['users']) == 0:
            if item.is_permanent:
                pass
            else:
                item.delete()
        pool[item.name] = load
    if request.method == 'POST':
        if 'room' in request.POST:
            form = CreateRoom(request.POST)
            if form.is_valid():
                former = form.save(commit=False)
                former.name = form.cleaned_data['name']
                former.description = form.cleaned_data['description']
                former.max_slots = form.cleaned_data['max_slots']
                former.host = request.user.username
                former.language_code = loc_option
                former.save()
                return HttpResponseRedirect(request.path_info)
    context = {
        'loc': loc_resolver('lobby'),
        'lang': loc_option,
        'room_list': room_list,
        'pool': pool,
        'room_form': room_form,
        'username': username
    }
    return HttpResponse(template.render(context, request))


def room(request, room_id):
    chat_form = SendMessage()
    room_info = Room.objects.get(id=room_id)
    template = loader.get_template('room.html')
    if request.user.is_authenticated:
        username = request.user.username
        loc_option = Hikka.objects.get(user=request.user.id).language_code
        authorised = True
    else:
        username = anonymous_validator(request)
        loc_option = 0
        authorised = False
    messages = Message.objects.filter(message_room__id=room_id).order_by('-pub_date')
    room_name = room_info.name
    if request.method == 'POST':
        if 'arch' in request.POST:
            make_chat_copy(room_id, room_name)
        elif 'leave' in request.POST:
            return HttpResponseRedirect(reverse('Chat:chat'))
        elif 'edit_description' in request.POST:
            form = EditDescription(request.POST, instance=room_info)
            if form.is_valid():
                room_info.description = form.cleaned_data['description']
                form.save()
                return HttpResponseRedirect(request.path_info)
        elif 'edit_room_name' in request.POST:
            form = EditName(request.POST, instance=room_info)
            if form.is_valid():
                former = form.save(commit=False)
                room_info.name = form.cleaned_data['name']
                former.save()
                return HttpResponseRedirect(request.path_info)
    context = {
        'edit_description_form': EditDescription(),
        'edit_name_form': EditName(),
        'loc': loc_resolver('room'),
        'lang': loc_option,
        'room_name': room_name,
        'messages': messages,
        'chat_form': chat_form,
        'username': username,
        'room_id': room_id,
        'authorised': authorised,
        'room_description': room_info.description,

    }
    return HttpResponse(template.render(context, request))


from django import forms
from .models import *


class SendMessage(forms.ModelForm):
    message_text = forms.CharField(label='Message Text', max_length=1000)

    class Meta:
        model = Message
        fields = ('message_text', )


class CreateRoom(forms.ModelForm):
    name = forms.CharField(label='Room name', max_length=100)
    description = forms.CharField(label='Room description', max_length=250)
    choices = [('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')]
    max_slots = forms.ChoiceField(choices=choices)

    class Meta:
        model = Room
        fields = ('name', 'description', 'max_slots',)


class EditDescription(forms.ModelForm):
    description = forms.CharField(label='Room description', max_length=200)

    class Meta:
        model = Room
        fields = ['description',]


class EditName(forms.ModelForm):
    name = forms.CharField(label='Room name', max_length=30)

    class Meta:
        model = Room
        fields = ['name',]

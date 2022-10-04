from django import forms
from .models import *


class SendMessage(forms.ModelForm):
    message_text = forms.CharField(label='Message Text', max_length=1000)

    class Meta:
        model = Message
        fields = ('message_text', )

from django import forms
from .models import *


class CreateMessage(forms.ModelForm):
    post_text = forms.CharField(label='Message', max_length=250, widget=forms.Textarea(attrs={
        'placeholder': 'Type your message here', 'rows': '1',
        'style': 'background: #454545; color: #f9f9f9;', 'class': 'form-control',
    }))

    class Meta:
        model = UserPublicPost
        fields = ('post_text', )

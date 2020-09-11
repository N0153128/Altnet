from django import forms
from .models import Thread, Comment


class CreateThread(forms.Form):
    thread_title = forms.CharField(label='Thread title', max_length=100)
    thread_text = forms.CharField(label='Thread text', max_length='5000', widget=forms.Textarea)
    choises = [('Random', 'Random'), ('Broadcast', 'Broadcast'), ('Animation', 'Animation'),
               ('Artwork', 'Artwork'), ('Cinematics', 'Cinematics'), ('Videogames', 'Videogames')]
    topic = forms.ChoiceField(choices=choises)


class ThreadForm(forms.ModelForm):

    thread_title = forms.CharField(label=False, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'background: #454545; color: #f9f9f9;', 'placeholder': 'Thread title'}))
    thread_text = forms.CharField(label=False, max_length='5000', widget=forms.Textarea(attrs={'style': 'background: #454545; color: #f9f9f9;', 'class': 'form-control', 'rows': '2.5', 'placeholder': 'Thread text'}),)
    choises = [('Random', 'Random'), ('Broadcast', 'Broadcast'), ('Animation', 'Animation'), ('Artwork', 'Artwork'),
               ('Cinematics', 'Cinematics'), ('Videogames', 'Videogames')]
    category = forms.ChoiceField(label=False, choices=choises, widget=forms.Select(attrs={'style':'background: #454545; color: #f9f9f9', 'class':'form-control'}))

    class Meta:
        model = Thread
        fields = ('thread_title', 'thread_text', 'category')


class CommentForm(forms.ModelForm):

    comment_text = forms.CharField(max_length=5000, widget=forms.Textarea(attrs={'style':'background: #454545; color: #f9f9f9;', 'class':'form-control', 'rows':'2.5', 'placeholder':'Start typing your comment here', }))
    key = forms.IntegerField(widget=forms.HiddenInput, required=False)

    class Meta:
        model = Comment
        fields = ('comment_text',)
from django.contrib import admin
from django import forms
from .models import Thread, Comment
from django.db import models


class ThreadForm(forms.ModelForm):
    thread_text = forms.CharField(widget=forms.Textarea(attrs={'rows': 10, 'cols': 55}))

    class Meta:
        model = Thread
        fields = '__all__'


class ThreadAdmin(admin.ModelAdmin):
    form = ThreadForm


class CommentForm(forms.ModelForm):
    comment_text = forms.CharField(widget=forms.Textarea(attrs={'rows': 10, 'cols': 55}))

    class Meta:
        model = Comment
        fields = '__all__'


class CommentAdmin(admin.ModelAdmin):
    form = CommentForm


admin.site.register(Thread, ThreadAdmin)
admin.site.register(Comment, CommentAdmin)

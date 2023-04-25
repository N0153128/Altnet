from django.contrib import admin
from django import forms
from .models import *
from django.db import models


@admin.action(description='Mark selected as visible')
def cat_make_visible(modeladmin, request, queryset):
    queryset.update(visible=True)


@admin.action(description='Mark selected as invisible')
def cat_make_invisible(modeladmin, request, queryset):
    queryset.update(visible=False)


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


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category', 'visible']
    ordering = ['category']
    actions = [cat_make_invisible, cat_make_visible]


admin.site.register(Thread, ThreadAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(PairMeta)

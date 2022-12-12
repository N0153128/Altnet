from django.contrib import admin
from .models import *
from django import forms


class PostForm(forms.ModelForm):
    post_text = forms.CharField(widget=forms.Textarea(attrs={'rows': 10, 'cols': 55}))

    class Meta:
        model = UserPublicPost
        fields = '__all__'


class PostAdmin(admin.ModelAdmin):
    form = PostForm


class AdminPostForm(forms.ModelForm):
    post_text = forms.CharField(widget=forms.Textarea(attrs={'rows': 10, 'cols': 55}))

    class Meta:
        model = AdminPublicPost
        fields = '__all__'


class AdminPostAdmin(admin.ModelAdmin):
    form = AdminPostForm


admin.site.register(Hikka)
admin.site.register(UserPublicPost, PostAdmin)
admin.site.register(ChangeLog)
admin.site.register(AdminPublicPost, AdminPostAdmin)
admin.site.register(Referral)
admin.site.register(Copy)
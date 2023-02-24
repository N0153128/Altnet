from .models import *
from django.db import models
from django.contrib import admin


admin.site.register(Room)
admin.site.register(Message)
admin.site.register(Pool)
admin.site.register(Ban)
admin.site.register(Role)
admin.site.register(Host)
admin.site.register(ChannelPair)



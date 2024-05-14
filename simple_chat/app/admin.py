from django.contrib import admin
from .models import Thread, Message

# add models to manipulate it via admin panel
admin.site.register(Thread)
admin.site.register(Message)

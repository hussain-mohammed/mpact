from django.contrib import admin
from .models import UserData, ChatData, UserChat

# Register your models here.
admin.site.register(UserData)
admin.site.register(ChatData)
admin.site.register(UserChat)

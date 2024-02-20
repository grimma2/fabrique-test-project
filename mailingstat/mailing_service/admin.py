from django.contrib import admin

from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'mailing', 'client', 'send_time', 'status')
    list_display_links = ('id', 'status', 'send_time')

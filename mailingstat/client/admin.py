from django.contrib import admin

from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone', 'operator_code', 'tag', 'timezone')
    list_display_links = ('id', 'phone')

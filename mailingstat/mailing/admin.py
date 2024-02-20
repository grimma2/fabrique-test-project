from django.contrib import admin

from .models import Mailing


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'start_time', 'end_time', 'message', 'filter_tag', 'filter_operator_code'
    )
    list_display_links = ('id', 'message')

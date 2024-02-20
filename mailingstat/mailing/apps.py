from django.apps import AppConfig
from django.db.models.signals import post_save


class MailingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mailing'

    def ready(self) -> None:
        from . import signals
        from mailing.models import Mailing
        post_save.connect(signals.trigger_mailing_task, sender=Mailing, dispatch_uid='post_save_mailing')


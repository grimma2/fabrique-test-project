from mailing_service.tasks import send_mailing_task

import logging


def trigger_mailing_task(sender, instance, created, **kwargs):
    if created:
        logging.getLogger('mailingsLogger').info(f'start task with {instance}')
        send_mailing_task.apply_async(kwargs={'mailing_id': instance.id}, eta=instance.start_time)

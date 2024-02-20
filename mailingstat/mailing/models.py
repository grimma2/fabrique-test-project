from django.db import models

from django.core.exceptions import ValidationError

import logging


class Mailing(models.Model):
    start_time = models.DateTimeField(verbose_name='Дата и время начала рассылки')
    end_time = models.DateTimeField(verbose_name='Дата и время окончания рассылки')
    message = models.TextField(verbose_name='Текст сообщения для рассылки')
    filter_tag = models.CharField(max_length=255, blank=True, null=True, verbose_name='Фильтр по тегу клиента')
    filter_operator_code = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Фильтр по коду оператора')
    send_start_time = models.TimeField('Начала интервала, в котором отправлять сообщения', blank=True, null=True)
    send_end_time = models.TimeField('Начала интервала, в котором отправлять сообщения', blank=True, null=True)

    def __str__(self):
        return f'message: {self.message}, start: {self.start_time}'

    def clean(self):
        if self.send_start_time or self.send_end_time:
            if not (self.send_start_time and self.send_end_time):
                raise ValidationError('Оба занчения интервала должны быть предоставлены, либо ни одного')
        else:
            return super().clean()

        if not self.send_start_time < self.send_end_time:
            raise ValidationError('Время начала интервала должно быть меньше, чем время окончания')

        logging.info(
            f'''
            save/update/create Mailing with attrs: 
            {self.start_time=}, {self.end_time=}, 
            {self.filter_tag=}, {self.filter_operator_code=},
            {self.send_start_time=}, {self.send_end_time=},
            {self.message=}
            '''
        )

        super().clean()

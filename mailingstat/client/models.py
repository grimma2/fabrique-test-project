from django.db import models
from django.core.exceptions import ValidationError

import pytz

import logging


class Client(models.Model):
    phone = models.CharField('Номер телефона клиента', max_length=11, unique=True)
    operator_code = models.PositiveSmallIntegerField('Код собильного оператора')
    tag = models.CharField('Произвольный тег клиента', max_length=255)
    timezone = models.CharField('Часовой пояс', max_length=50, choices=[(tz, tz) for tz in pytz.all_timezones])

    def __str__(self) -> str:
        return self.phone

    def clean(self):
        if not self.phone.startswith('7'):
            raise ValidationError({'phone': "Phone number must start with '7'."})
        
        if not self.phone.isdigit():
            raise ValidationError({'phone': "Phone number must contain only numbers."})
        
        if len(self.phone) != 11:
            raise ValidationError('Phone number should be lenght 11')

        logging.info(
            f'save/update/create Client with attrs: {self.phone}, {self.operator_code}, {self.tag}, {self.timezone}'
        )

        super().clean()

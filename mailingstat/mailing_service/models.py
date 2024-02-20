from django.db import models

from mailing.models import Mailing
from client.models import Client


class Message(models.Model):
    STATUS_CHOICES = [
        ('sent', 'Отправлено'),
        ('failed', 'Не удалось отправить'),
    ]

    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, related_name='messages', verbose_name='Рассылка')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='messages', verbose_name='Клиент')
    send_time = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время отправки')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='sent', verbose_name='Статус отправки')

    def __str__(self):
        return f"{self.mailing.id} mailing to {self.client.phone} client"

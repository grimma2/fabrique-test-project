# Generated by Django 5.0.2 on 2024-02-18 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Mailing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(verbose_name='Дата и время начала рассылки')),
                ('end_time', models.DateTimeField(verbose_name='Дата и время окончания рассылки')),
                ('message', models.TextField(verbose_name='Текст сообщения для рассылки')),
                ('filter_tag', models.CharField(blank=True, max_length=255, null=True, verbose_name='Фильтр по тегу клиента')),
                ('filter_operator_code', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Фильтр по коду оператора')),
            ],
        ),
    ]
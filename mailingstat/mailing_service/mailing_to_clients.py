from django.utils.timezone import now

from client.models import Client
from mailingstat.settings import CELERY_BROKER_URL
from mailing.models import Mailing
from .models import Message
from .exponentinal_backoff import ExponentialBackoff
from .exceptions import InvalidDataAnswer, MaxRetries

from dataclasses import dataclass, field
import json
import os
import logging
from datetime import datetime, timezone

import aio_pika
import httpx
import asyncio
import pytz


@dataclass
class MailingProcesser(ExponentialBackoff):
    mailing: Mailing = field(default_factory=int)

    async def process_mailing(self):
        connection = await aio_pika.connect_robust(CELERY_BROKER_URL)

        async with connection:
            channel = await connection.channel()
            
            queue_name = f'mailing_{self.mailing.id}'
            self.queue_name = queue_name
            
            queue = await channel.declare_queue(queue_name, durable=True, auto_delete=True)
            
            if self.mailing.filter_operator_code:
                clients = Client.objects.filter(operator_code=self.mailing.filter_operator_code)
            else:
                clients = Client.objects.all()
            
            if self.mailing.filter_tag:
                clients = clients.filter(tag=self.mailing.filter_tag)
            
            async for client in clients:
                message_data = {
                    'end_time': self.mailing.end_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
                    'mailing_id': self.mailing.id,
                    'message_text': self.mailing.message,
                    'phone': client.phone,
                    'timezone': client.timezone,
                    'retries': 0
                }

                await channel.default_exchange.publish(
                    aio_pika.Message(body=json.dumps(message_data).encode()),
                    routing_key=queue.name,
                )
            
            self.queue_messages_count = len(clients)
            
            await queue.consume(self.callback)
            self.connection = connection
            self.channel = channel

            self.future = asyncio.Future()

            try:
                await self.future  # Wait for the future to be completed or cancelled
            finally:
                if not self.future.done():
                    self.future.cancel()  # Ensure the future is cancelled to avoid blocking
                await connection.close()

    async def callback(self, message: aio_pika.IncomingMessage):
        async with message.process(ignore_processed=True):
            queue_message = json.loads(message.body)
            self.queue_message = queue_message

            end_time = datetime.strptime(queue_message['end_time'], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)
            if now() >= end_time:
                logging.getLogger('messagesLogger').info('stop mailing because mailing has end')
                if not self.future.done():
                    self.future.set_result(None)
                    return

            client_tz = pytz.timezone(queue_message['timezone'])
            now_local = now().astimezone(client_tz)

            if self.mailing.send_start_time and self.mailing.send_end_time:
                logging.info('check time gap')
                if not (self.mailing.send_start_time <= now_local.time() <= self.mailing.send_end_time):
                    logging.getLogger('messagesLogger').info('stop mailing because not fit in client`s time')
                    await message.reject()
                    return

            current_client = await Client.objects.aget(phone=queue_message['phone'])
            message_model = await Message.objects.acreate(
                mailing=self.mailing,
                client=current_client
            )

            try:
                await self.execute_with_backoff(self.make_request, message_model, message)
            except MaxRetries as e:
                logging.getLogger('messagesLogger').error(f'MaxRetries: {e}')

                if queue_message['retries'] < 10:
                    await message.reject()
                    await self.channel.default_exchange.publish(
                        aio_pika.Message(body=json.dumps(queue_message).encode()),
                        routing_key=self.queue_name,
                    )
                else:
                    logging.getLogger('messagesLogger').error(
                        f'reach max retries ({queue_message['retries']}) for message: {queue_message} and reject message'
                    )
                    await message.reject()
                    await self.decrement_messages()
            else:
                await self.decrement_messages()

    async def make_request(self, message_model: Message, message: aio_pika.IncomingMessage):
        async with httpx.AsyncClient() as client:
            logging.getLogger('messagesLogger').info(f'send message {message_model.id} with queue message: {self.queue_message}')
            response = await client.post(
                url=f'{os.environ['EXTERNAL_API_URL']}/send/{message_model.id}',
                json={
                    'id': message_model.id,
                    'text': self.queue_message['message_text'],
                    'phone': self.queue_message['phone']
                },
                headers={
                    'Authorization': f'Bearer {os.environ['AUTH_TOKEN']}'
                }
            )

        logging.getLogger('messagesLogger').info(f'send message response: {response.text}')

        if response.status_code == 200:
            await message.ack()
        elif response.status_code == 400:
            message_model.status = 'failed'
            await message_model.asave()
            await message.reject()
        elif response.status_code == 401:
            message_model.status = 'failed'
            await message_model.asave()
            if not self.future.done():
                self.future.set_result(None)
        else:
            logging.getLogger('messagesLogger').error(f'unknown error on message request: {response.text}, {response.status_code}')
            raise InvalidDataAnswer('Не получилось сохранить сообщение')

    async def decrement_messages(self):
        self.queue_messages_count -= 1
        if not self.queue_messages_count:
            if not self.future.done():
                self.future.set_result(None)

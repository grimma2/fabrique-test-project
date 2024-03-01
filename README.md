## Как запустить
 1. Создать виртуальное окружение python <code>py -m venv venv</code>
 2. Установить все зависимости <code>pip install -r requirements.txt</code>
 3. Запустить миграции <code>python manage.py migrate</code>
 4. Перейти в директорию mailingstat/ и запустить Django проект <code>python manage.py runserver</code>
 5. Использовать RabbitMQ в docker командой <code>docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq</code>
 6. В той же директории запустить Celery <code>celery -A mailingstat worker -l info</code>

Администраторский UI по адресу admin/

## Документация по API (так же есть swagger по адресу docs/):
### Приложение client
<code>POST /api/v1/client/add</code>
Добавляет запись клиента со всеми полями
#### Пример тела запроса:
<code>
{
    "phone": "79999999999",
    "operator_code": 999,
    "tag": "string",
    "timezone": "Antarctida/South_pole"
}
</code>
----
<code>PATCH /api/v1/client/update/{id}</code>
Изменяет клиента по его id и все поля являются опциональными
#### Пример тела запроса:
<code>
{
    "phone": "79999999999"
}
</code>
<code>PUT /api/v1/client/update/{id}</code>
Изменяет клиента по его id, при этом, все поля обязательны
#### Пример тела запроса:
<code>
{
    "phone": "79999999999",
    "operator_code": 999,
    "tag": "string",
    "timezone": "Antarctida/South_pole"
}
</code>
----
<code>DELETE /api/v1/client/delete/{id}</code>
Удаляет клиента по его id
### Приложение mailing
<code>POST /api/v1/mailing/add</code>
Добавляет рассылку вместе со всеми её атрибутами и celery task, которы запускается в момент начала рассылки
#### Пример тела запроса:
<code>
{
  "start_time": "2024-02-20T19:29:19.504Z",
  "end_time": "2024-02-20T19:29:19.504Z",
  "message": "string",
  "filter_tag": "string",
  "filter_operator_code": 9223372036854776000,
  "send_start_time": "string",
  "send_end_time": "string"
}
</code>
----
<code>PATCH /api/v1/mailing/update/{id}</code>
Изменяет рассылку по её id, при этом все параметры опциональны
#### Пример тела запроса:
<code>
{
  "filter_tag": "string"
}
</code>
----
<code>PUT /api/v1/mailing/update/{id}</code>
Изменяет рассылку по её id, при этом все параметры обязательны
#### Пример тела запроса:
<code>
{
  "start_time": "2024-02-20T19:29:19.504Z",
  "end_time": "2024-02-20T19:29:19.504Z",
  "message": "string",
  "filter_tag": "string",
  "filter_operator_code": 9223372036854776000,
  "send_start_time": "string",
  "send_end_time": "string"
}
</code>
----
<code>DELETE /api/v1/client/delete/{id}</code>
Удаляет рассылку по её id
----
<code>GET /api/v1/mailing/stats</code>
Возвращает общую статистику по всем рассылкам (массив рассылок и у каждой ключи 'fail' и 'sent' с количеством отправленных сообщений успешно и не успешно)
----
<code>GET /api/v1/mailing/stats/{id}</code>
Возвращает подробную статистику по одной рассылке (список всех сообщений, которые были отправленные во время этой рассылки)### Приложение client

## Выполненые дополнительные задания
 - Пункт 5 (swagger по адресу /docs/)
 - Пункт 6 (реализовать административный Web-UI)
 - Пункт 9 (Повторные запросы при некоректном ответе сервера. Сделал экпоненциальную задержку в отправке запросов на сервер, если же не получилось отправить, то добавляю клиента в конец очереди для повторной отпрвки. При этом реализована асинхронная отправка запросов на сервер, обращение в бд и работа с очередью сообщений RabbitMQ, для того, чтобы задержки в ответе сервера не мешали работе рассылки)
 - Пункт 11 (дополнительная логика, которая учитваем время пользователя и не отправляет сообщение, если текущее время вне временного интервала)
 - Пункт 12 (Подробное логирование всех действий с клиентом, рассылкой и сообщениями в файлах clients.log, mailings.log, messages.log)

## Стек приложения
 - Python, DRF, aio-pika, Celery (RabbitMQ в качестве брокера сообщений для Celery и очереди, куда добавляются клиенты для рассылок)

# VTP_API_Hackathon_Foxhound_team
Решение команды Foxhound на хакатоне VTB API 2021

## Описание приложения

Решение команды Foxhound представляет собой сервис для проверки контента передаваемого по WebSocket, а также для проверки файлов.

Здесь представлены три модуля: 
- Интерфейс администрирования
- WebSocket сервис
- Сервис проверки файлов

## Инструкция по запуску
Демо решение расположено по адресу [](адрес)

Логин: admin

Пароль: 1234

Для запуска локально, см. [Развертывание через docker-compose](#развертывание-через-docker-compose)

## Описание системы
### Интерфейс администрирования
Интерфейс содержит следующие вкладки:
- Дашборд
- WebSocket
    - Нарушения
    - Схемы
    - Обратные вызовы
- Файлы
    - Проверки
    - Разрешенные файлы
    - Прокси
- Настройки
#### Дашборд
На данной вкладке представлена краткая аналитика по нарушениям. 
На графике отображается количество различных нарушений за выбранный период.

Также на вкладке представлены две мини таблицы, которые отображают файловые нарушения и нарушения websocket.
#### Websocket
##### Нарушения
Вкладка содержит таблицу со всеми нарушениями websocket, каждую запись можно просматривать более подробно.
##### Схемы
На данной вкладке производится настройка JSON схем для передачи по WebSocket.

В схеме указывается метод, для которого она будет использоваться, а также строится сама JSON схема для валидации сообщения.
#### Обратные вызовы
**Обратные вызовы** это http методы, которые вызываются для сообщений по WebSocket для определенных методов.

Текущая вкладка отображает таблицу обратных вызовов и позволяет создавать новые.
### Файлы
#### Проверки
Здесь отображаются загруженные файлы пользователей, а также статус их проверки. Каждую запись можно просматривать более подробно.
#### Разрешенные файлы
В этой вкладке настраиваются разрешенные типы файлов, их максимальная глубина (при наличии), а также максимальный размер.
#### Прокси
Прокси используется для отправки ссылки на файл определенным сервисам.
### Настройки
Здесь можно настроить разрешенные WebSocket Origins.

## Получение JWT токена
Для получения JWT токена необходимо вызвать следующий метод
`POST /rest_api/auth/api-token-auth/`
С телом запроса
```json
{
    "username": "username",
    "password": "password"
}
```
В ответ вернется токен:
```json
{
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFkbWluIiwiZXhwIjoxNjM4ODkwNTA5LCJlbWFpbCI6ImFkbWluQGV4YW1wbGUuY29tIn0.aAhzK3iDjoaxN0T0B_HXJbiT7q0Z9G_xL1_AzZ4s6Z0"
}
```

## Описание WebSocket взаимодействий
### Структура WebSocket сообщения
WebSocket сообщения должны быть представлены в JSON формате и иметь следующие обязательные поля:
- token - [JWT токен](#получение-JWT-токена)
- method - метод, по которому будет проходить валидация и вызываться [обратный вызов](#обратные-вызовы)
- payload - передаваемые данные, которые будут проходить валидацию по [JSON схеме](#схемы)

Пример:
```json
{
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFkbWluIiwiZXhwIjoxNjM4ODkwNTA5LCJlbWFpbCI6ImFkbWluQGV4YW1wbGUuY29tIn0.aAhzK3iDjoaxN0T0B_HXJbiT7q0Z9G_xL1_AzZ4s6Z0",
    "method": "chat",
    "paload": {
        "message": "Hello world!",
        "chat_id": 1
    }
}
``` 
### Использование WebSocket на клиенте
Для общения по WebSocket необходимо использовать открытую библиотеку [socket.io](https://socket.io).

Пример использования:
```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js" integrity="sha512-q/dWJ3kcmjBLU4Qc47E4A9kTB4m3wuTY7vkFJDTZKjTs8jhyGQnaUrxa0Ytd0ssMZhbNua9hE+E7Qv1j+DyZwA==" crossorigin="anonymous"></script>
<script type="text/javascript" charset="utf-8">

    var socket = io("https://some.socket.domain", {query: { token: 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFkbWluIiwiZXhwIjoxNjM4ODkwNTA5LCJlbWFpbCI6ImFkbWluQGV4YW1wbGUuY29tIn0.aAhzK3iDjoaxN0T0B_HXJbiT7q0Z9G_xL1_AzZ4s6Z0' }, transports: ['websocket']});
    socket.on("reply", (data) => {
        console.log(data)
    })
    socket.send(
        {
            "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFkbWluIiwiZXhwIjoxNjM4ODkwNTA5LCJlbWFpbCI6ImFkbWluQGV4YW1wbGUuY29tIn0.aAhzK3iDjoaxN0T0B_HXJbiT7q0Z9G_xL1_AzZ4s6Z0",
            "method": "chat",
            "paload": {
                "message": "Hello world!",
                "chat_id": 1
            }
        }
    );
</script>
```
### HTTP взаимодействие с backend
HTTP взаимодействие построено на вызове [обратных функций](#обратные-вызовы) для методов.

Например можно настроить, чтобы при получении сообщения с методом "chat" вызывался метод на backend POST http://example.com/callback/

Отсылаемое сообщение будет содержать следующие поля:
- client - информация об авторизованном пользователе
- method - метод, который был вызван (в данном случае "chat")
- payload - данные, которые отправил пользователь (данные из payload поля WebSocket)

Для публикации сообщений с backend необходимо вызывать следующий метод

POST /api

Параметры:
- token - [авторизационный токен сервера](#SERVER_TOKEN)
- method - канал (метод) в который нужно опубликовать сообщение
- payload - данные, которые нужно опубликовать

Пример запроса:
```json
{
    "token": "SECTET_SERVER_TOKEN",
    "method": "reply",
    "payload": {
        "message": "Hello from server",
        "chat_id": 1
    }
}
```

## Описание API для проверки файлов
Для проверки файла, необходимо вызвать следующий метод:

POST /rest_api/file/

Параметры:
- file - файл, который нужно проверить

Также ссылка для проверки статуса файла будет отправлена на [файловые прокси](#прокси), которые можно настроить в интерфейсе администрирования.

Формат сообщения:
- url - ссылка для получения информации о проверке файла и ссылки на скачивание
- status - статус проверки (сразу после загрузки == P - в процессе)

После загрузки файла запускается проверка в асинхронном режиме. По завершении проверки ссылка и статус проверки будут отправлены ещё раз на все файловые прокси.

Формат сообщения о состоянии файла:
- file_url - ссылка для скачивания файла
- name - оригинальное название файла
- source - IP адрес отправителя файла
- client - ID и логин отправителя
- dttm_loaded - дата и время загрузки файла
- dttm_end_check - дата и время завершения проверки
- status - статус проверки (возможные значения P - в процессе, O - ОК, V - нарушение, E - ошибка проверки)
- message - сообщение с информацией о проверке, в случае успешной проверки, поле пустое
- file_type - распознанный тип файла

Пример сообщения о состоянии файла:
```json
{
    "id": 2,
    "file_url": "https:/example.com/media/files/a1aecfe2-7cac-4d21-a862-e01cefcd3109.pdf",
    "name": "Academic articles writing and analysis_Lecture 8_Results.pdf",
    "source": "171.11.23.5",
    "client": "1 admin",
    "dttm_loaded": "2021-12-07T17:52:01.049682",
    "dttm_end_check": null,
    "status": "P",
    "message": null,
    "file_type": "pdf"
}
```


## Развертывание через docker-compose
1. Установить [docker](https://docs.docker.com/engine/install/ubuntu/)
2. Установить [docker-compose](https://docs.docker.com/compose/install/)
3. В папке compose создать файлы .env, .websocket.env и .backend.env и [заполнить](#описание-переменных-окружения) их в соответствии с примерами
4. Запустить команду docker-compose up -d с правами суперпользователя
```bash
sudo docker-compose up -d
```
5. Настроить внешний nginx, который будет пересылать все запросы на порт приложения
6. Создать аккаунт администратора командой 
```bash
sudo docker-compose exec backend python manage.py createsuperuser
```
## Описание переменных окружения

### HTTP_PORT
Файлы: .env

Тип: целое число

Назначение: порт на котором будет крутиться приложение
### UWSGI_WORKERS
Файлы: .backend.env, .websocket.env

Тип: целое число

Назначение: количество процессов UWSGI

### UWSGI_THREADS
Файлы: .backend.env, .websocket.env

Тип: целое число

Назначение: количество потоков UWSGI
### JWT_SECRET
Файлы: .backend.env, .websocket.env

Тип: строка

Назначение: секретное значение для генерации JWT токенов
### EXTERNAL_HOST
Файлы: .backend.env

Тип: строка

Назначение: хост, который будет подставляться к урлам для скачивания и проверки статусов файлов
### SERVER_TOKEN
Файлы: .websocket.env

Тип: строка

Назначение: секретный токен для авторизации сервера по HTTP

## Команды docker-compose 
Все команды необходимо выполнять в папке compose
- Остановить все контейнеры
```bash
sudo docker-compose stop
```
- Перезапустить контейнер
```bash
sudo docker-compose restart {container_name}
```
- Запуск manage.py shell
```bash
sudo docker-compose exec backend python manage.py shell
```

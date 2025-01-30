import time
from telethon import TelegramClient, events
from telethon.errors import SessionPasswordNeededError

# Ваши настройки
api_id = 26942711
api_hash = '5ca79b214c4d482bafb891e970392222'

# Запрашиваем номер телефона
phone_number = input("Введите номер телефона в формате +1234567890: ")

# Инициализация клиента
client = TelegramClient('session_name', api_id, api_hash)

async def main():
    await client.start(phone_number)  # Логин с вашим номером телефона

    # Обработка входящих сообщений
    @client.on(events.NewMessage)
    async def handle_new_message(event):
        sender = await event.get_sender()  # Получаем информацию о пользователе
        sender_name = "Unknown"

        if sender:
            sender_name = sender.username if sender.username else "Unknown"

        print(f"Новое сообщение от {sender_name}: {event.text}")

    # Обработка удалённых сообщений
    @client.on(events.MessageDeleted)
    async def handle_deleted_message(event):
        print(f"Сообщение удалено: {event.deleted_ids}")
    
    # Обработка двухфакторной аутентификации и пароля
    try:
        await client.start(phone_number)

        # Запрашиваем код подтверждения при необходимости
        if not await client.is_user_authorized():
            print("Введите код подтверждения из SMS")
            code = input("Введите код: ")
            await client.sign_in(phone_number, code)

            # Если нужен пароль
            if isinstance(await client.get_me(), SessionPasswordNeededError):
                password = input("Введите пароль: ")
                await client.sign_in(password=password)

        # Запуск бота и обработка событий
        print("Бот запущен, ждёт сообщений и удалений...")
        await client.run_until_disconnected()  # Ожидание событий
    except KeyboardInterrupt:
        print("Бот был остановлен вручную.")
        await client.disconnect()  # Отключение клиента
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        await client.disconnect()  # Отключение клиента

if __name__ == '__main__':
    client.loop.run_until_complete(main())
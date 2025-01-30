from telethon import TelegramClient, events
import asyncio

# ТВОИ ДАННЫЕ
API_ID = 27789604  # Твой API ID
API_HASH = 'b581e0c88c2715b5b42a9e7073d21a2f'  # Твой API HASH
ARCHIVE_BOT_ID = 777000  # ID бота-архиватора (замени на правильный ID)

# Создаем клиент
client = TelegramClient('my_session', API_ID, API_HASH)

# Хранилище сообщений {message_id: (sender_name, text, media)}
message_storage = {}

# Обработчик входящих сообщений (запоминаем их)
@client.on(events.NewMessage)
async def handle_new_message(event):
    sender = await event.get_sender()
    sender_name = sender.username if sender.username else "Unknown"
    text = event.message.text or "Нет текста"
    media = event.message.media if event.message.media else None  # Получаем медиа (если есть)

    # Запоминаем сообщение
    message_storage[event.message.id] = (sender_name, text, media)

    print(f"Сообщение получено от {sender_name}: {text}")
    if media:
        print(f"С медиа: {media}")

# Обработчик удаленных сообщений (поддержка множественных удалений)
@client.on(events.MessageDeleted)
async def handle_deleted_message(event):
    for msg_id in event.message_ids:
        if msg_id in message_storage:
            sender_name, message_content, media = message_storage[msg_id]
            print(f"Сообщение удалено от {sender_name}: {message_content}")

            # Отправляем удаленное сообщение в архивный бот
            if media:
                # Если есть медиа
                await client.send_file(ARCHIVE_BOT_ID, media, caption=message_content)
            else:
                # Если медиа нет
                await client.send_message(ARCHIVE_BOT_ID, message_content)

# Запускаем клиент
async def main():
    await client.start()
    print("Бот запущен, ждем сообщений и удалений...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
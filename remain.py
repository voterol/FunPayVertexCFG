from telethon import TelegramClient, events
import asyncio

# ТВОИ ДАННЫЕ
API_ID = 27789604  # Твой API ID
API_HASH = 'b581e0c88c2715b5b42a9e7073d21a2f'  # Твой API HASH
ARCHIVE_BOT_ID = 777000  # ID бота-архиватора

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
    media = None  # По умолчанию нет медиа

    # Проверяем наличие вложений (фото, видео и т.д.)
    if event.message.media:
        media = event.message.media

    # Запоминаем сообщение
    message_storage[event.message.id] = (sender_name, text, media)

# Обработчик удаления сообщений (отправляем в архив)
@client.on(events.MessageDeleted)
async def handle_deleted_message(event):
    for msg_id in event.message_ids:  # Обрабатываем все удаленные сообщения
        if msg_id in message_storage:
            sender_name, text, media = message_storage.pop(msg_id)  # Достаем сообщение из памяти

            # Отправляем текст в архив
            message_content = f"‼️ Сообщение удалено!\n\nFrom: {sender_name}\n{text}"

            # Если есть медиа, отправляем его в архивный бот
            if media:
                try:
                    # Отправка с вложением (фото, видео и т.д.)
                    await client.send_file(ARCHIVE_BOT_ID, media, caption=message_content)
                except Exception as e:
                    print(f"Ошибка при отправке медиа: {e}")
            else:
                # Если нет медиа, отправляем только текст
                await client.send_message(ARCHIVE_BOT_ID, message_content)

# Запуск бота
async def main():
    print("Бот запущен, ждёт сообщений и удалений...")
    await client.start()
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
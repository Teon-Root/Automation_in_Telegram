import asyncio
from telethon import TelegramClient, events
from dotenv import load_dotenv
import os


load_dotenv()
api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')
api_bot_token = os.getenv('BOT_TOKEN')
admin_id = int(os.getenv('ADMIN_ID'))
group_links = os.getenv('GROUP_LINK')

bot = TelegramClient('bot', api_id, api_hash).start(bot_token=api_bot_token)


async def start():
    await bot.send_message(admin_id, 'Бот запустился, привет Админ!')


loop = asyncio.get_event_loop()
loop.run_until_complete(start())


@bot.on(events.NewMessage(pattern='/start'))
async def send_welcome(event):
    await event.reply('Ответ на START')


@bot.on(events.NewMessage(pattern='(^cat[s]?$|puss)'))
async def cats(event):
    await event.reply('Котик 😺')

keywords = ["добрый день", "привет", "помогите", "пожалуйста", "работа", "день", "в чому",
            "проблема", "памогите", "почему", "чому", "Підскажіть", "подскажите",
            "Кто знает", "может кто", "Доброго", "привіт", "ищу", "шукаю", "добрий",
            "добрый"]

client = TelegramClient('anon', api_id, api_hash)


@client.on(events.NewMessage(chats=group_links))
async def my_event_handler(event):
    sender = await event.get_sender()
    chat_title = event.chat.title if event.chat else "Неизвестная группа"
    if sender is not None:
        sender_username = sender.username
        sender_id = sender.id

        if sender_username:
            sender_link = f"https://t.me/{sender_username}"
        else:
            sender_link = f"tg://user?id={sender_id}"
    else:
        sender_link = "Аноним"

    chat_id = event.chat_id
    message_id = event.message.id

    if str(chat_id).startswith('-100'):
        message_link = f"https://t.me/c/{str(chat_id)[4:]}/{message_id}"
    else:
        message_link = f"https://t.me/c/{chat_id}/{message_id}"

    message_text = event.raw_text.lower()
    if any(keyword in message_text for keyword in keywords):
        await bot.send_message(
            admin_id,
            f'💌 "{chat_title}" от {sender_link}:\n\n'
            f'{event.raw_text}\n\n'
            f'Ссылка на сообщение: {message_link}'
        )


client.start()
client.run_until_disconnected()



if __name__ == '__main__':
    bot.run_until_disconnected()

import os
import telebot
from datetime import datetime

TOKEN = os.getenv("BOT_TOKEN", "ВСТАВЬ_СВОЙ_ТОКЕН_ОТСЮДА")  # замени на свой токен

bot = telebot.TeleBot(TOKEN)

user_messages = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет 👋 Это бот «Письма себе».\nНапиши сюда письмо самому себе, я сохраню его и отправлю тебе обратно через время ⏳")

@bot.message_handler(commands=['read'])
def read_letter(message):
    chat_id = message.chat.id
    if chat_id in user_messages:
        bot.reply_to(message, f"📬 Вот твоё письмо:\n\n{user_messages[chat_id]['text']}\n\n✉️ Написано: {user_messages[chat_id]['time']}")
    else:
        bot.reply_to(message, "У тебя пока нет писем. Напиши новое!")

@bot.message_handler(func=lambda message: True)
def save_letter(message):
    chat_id = message.chat.id
    user_messages[chat_id] = {
        "text": message.text,
        "time": datetime.now().strftime("%d.%m.%Y %H:%M")
    }
    bot.reply_to(message, "✏️ Я сохранил твоё письмо. Позже сможешь его прочитать командой /read.")

bot.polling()

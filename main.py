import logging
from aiogram import Bot, Dispatcher, executor, types
import openai
import os

# Вставь сюда свой токен от Telegram
BOT_TOKEN = 7000374618:AAEYOKpZKyV-nkelONeNnt4H2r-AimCstWE
# Вставь сюда свой OpenAI API-ключ
OPENAI_API_KEY = сюда_вставь_свой_openAI_API_KEY"

openai.api_key = OPENAI_API_KEY

# Настройки логирования
logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Привет! 👋 Я бот 'Письма себе'. Напиши мне сообщение — и я помогу тебе разобраться в себе.")

@dp.message_handler()
async def talk_with_ai(message: types.Message):
    user_text = message.text

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты — тёплый, вдумчивый собеседник. Помогай пользователю понять себя, поддерживай и задавай мягкие вопросы."},
                {"role": "user", "content": user_text}
            ]
        )

        reply = response.choices[0].message["content"]
        await message.answer(reply)

    except Exception as e:
        await message.answer("Произошла ошибка 😔 Попробуй позже.")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

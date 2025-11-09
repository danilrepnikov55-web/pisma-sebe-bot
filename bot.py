import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
import os

# Загружаем токен
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
scheduler = AsyncIOScheduler()

# Простое хранилище (можно заменить на базу)
letters = {}

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "👋 Привет!\n\n"
        "Я — твой почтальон во времени ⏳\n\n"
        "✉️ Напиши письмо, которое хочешь отправить себе в будущее."
    )
    letters[message.from_user.id] = {"stage": "waiting_text"}

@dp.message()
async def handle_message(message: types.Message):
    user_id = message.from_user.id
    user_data = letters.get(user_id, {})

    if user_data.get("stage") == "waiting_text":
        letters[user_id]["text"] = message.text
        letters[user_id]["stage"] = "waiting_date"
        await message.answer(
            "📅 Отлично! Теперь напиши дату и время, когда я должен доставить письмо.\n"
            "Формат: `ДД.ММ.ГГГГ ЧЧ:ММ`"
        )

    elif user_data.get("stage") == "waiting_date":
        try:
            send_time = datetime.strptime(message.text, "%d.%m.%Y %H:%M")
            text = user_data["text"]
            letters[user_id]["stage"] = None

            scheduler.add_job(
                send_letter,
                trigger="date",
                run_date=send_time,
                args=[user_id, text]
            )

            await message.answer(
                f"🕊 Письмо сохранено!\n"
                f"Я отправлю его тебе {send_time.strftime('%d %B %Y в %H:%M')} 💫"
            )
        except ValueError:
            await message.answer("⚠️ Неверный формат даты. Попробуй снова: `ДД.ММ.ГГГГ ЧЧ:ММ`")

async def send_letter(user_id: int, text: str):
    await bot.send_message(
        user_id,
        f"⏳ Время пришло!\n\n"
        f"Вот твоё письмо из прошлого 💌\n\n> {text}"
    )

async def main():
    scheduler.start()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

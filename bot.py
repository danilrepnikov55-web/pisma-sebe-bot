import os
import asyncio
from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from apscheduler.schedulers.asyncio import AsyncIOScheduler

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
scheduler = AsyncIOScheduler()

letters = {}

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("💌 Привет! Я — бот, который доставит твоё письмо в будущее ✨\n"
                         "Хочешь попробовать? Напиши /letter")

@dp.message(Command("letter"))
async def new_letter(message: types.Message):
    await message.answer("📝 Напиши своё письмо себе в будущее:")
    letters[message.from_user.id] = {"step": "text"}

@dp.message()
async def handle_message(message: types.Message):
    user_id = message.from_user.id

    if user_id in letters and letters[user_id]["step"] == "text":
        letters[user_id]["text"] = message.text
        letters[user_id]["step"] = "date"
        await message.answer("⏰ Отлично! Теперь напиши дату и время доставки в формате YYYY-MM-DD HH:MM\n"
                             "Например: 2025-12-31 20:00")
        return

    if user_id in letters and letters[user_id]["step"] == "date":
        try:
            send_time = datetime.strptime(message.text, "%Y-%m-%d %H:%M")
            text = letters[user_id]["text"]

            scheduler.add_job(send_letter, "date", run_date=send_time, args=(user_id, text))
            letters.pop(user_id)

            await message.answer(f"✨ Письмо сохранено!\n"
                                 f"Я пришлю его тебе {send_time.strftime('%d.%m.%Y в %H:%M')} 💫")
        except ValueError:
            await message.answer("⚠️ Формат неверный! Попробуй ещё раз, например: 2025-12-31 20:00")

async def send_letter(user_id, text):
    await bot.send_message(user_id, f"📬 Твоё письмо из прошлого:\n\n{text}")

async def main():
    scheduler.start()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

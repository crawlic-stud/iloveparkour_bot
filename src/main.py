import asyncio
import os
import logging
import io
from pathlib import Path
import random

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import IDFilter
from dotenv import load_dotenv
import aioschedule

import messages


load_dotenv()
bot = Bot(os.getenv("TOKEN"), parse_mode="HTML")
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

minapova_id = int(os.getenv("MINAPOVA_ID"))
admin_id = int(os.getenv("ADMIN_ID"))
ids = [minapova_id, admin_id]


async def send_message(path: Path):
    text = messages.extract_random_text(path, random.randint(1, 3))
    pic_path = messages.get_picture()
    message = messages.get_message(text)
    for each in ids:
        # for each in [admin_id]:
        fbytes = io.BytesIO(pic_path.read_bytes())
        file_ = types.InputFile(fbytes, "wazowski.png")
        await bot.send_photo(each, file_, message)
    print("sent!")


async def loop():
    aioschedule.every().day.at("5:30").do(
        send_message, messages.TEXTS_PATH / 'morning.txt')
    aioschedule.every().day.at("10:00").do(
        send_message, messages.TEXTS_PATH / 'day.txt')
    aioschedule.every().day.at("14:30").do(
        send_message, messages.TEXTS_PATH / 'evening.txt')
    aioschedule.every().day.at("19:00").do(
        send_message, messages.TEXTS_PATH / 'night.txt')
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(*args, **kwargs):
    asyncio.create_task(loop())


@dp.message_handler(IDFilter(user_id=ids))
async def hello(msg: types.Message):
    print(f"{msg.from_id=}, {msg.text=}")
    # await msg.answer(get_message())


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

import asyncio
import os
import logging
import io
from pathlib import Path
import random
from typing import Callable

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
jobs = {}


async def send_message(path: Path, tag: str, hour: str):
    text = messages.extract_random_text(path, random.randint(1, 3))
    pic_path = messages.get_picture()
    message = messages.get_message(text)
    for each in ids:
        # for each in [admin_id]:
        fbytes = io.BytesIO(pic_path.read_bytes())
        file_ = types.InputFile(fbytes, "wazowski.png")
        await bot.send_photo(each, file_, message)
    print("sent!")
    await schedule_job_randomly(send_message, path, tag, hour)


def run_every_day(at: str, *args, **kwargs):
    return aioschedule.every().day.at(at).do(*args, **kwargs)


async def schedule_job_randomly(job: Callable, path: Path, tag: str, hour: str):
    minutes = random.randint(1, 59)
    new_time = f"{hour}:{str(minutes).zfill(2)}"
    if jobs.get(tag):
        aioschedule.cancel_job(jobs[tag])
    jobs[tag] = run_every_day(
        new_time,
        job,
        path=path,
        tag=tag,
        hour=hour)
    print(aioschedule.jobs)
    return jobs[tag]


async def loop():
    await schedule_job_randomly(send_message,
                                path=messages.TEXTS_PATH / 'morning.txt',
                                tag="morning",
                                hour="5")
    await schedule_job_randomly(send_message,
                                path=messages.TEXTS_PATH / 'day.txt',
                                tag="day",
                                hour="10")
    await schedule_job_randomly(send_message,
                                path=messages.TEXTS_PATH / 'evening.txt',
                                tag="evening",
                                hour="14")
    await schedule_job_randomly(send_message,
                                path=messages.TEXTS_PATH / 'night.txt',
                                tag="night",
                                hour="19")
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

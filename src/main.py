import asyncio
import os
import logging
import io

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import IDFilter
from dotenv import load_dotenv
import aioschedule

from message import get_message, get_picture


load_dotenv()
bot = Bot(os.getenv("TOKEN"), parse_mode="HTML")
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

minapova_id = int(os.getenv("MINAPOVA_ID"))
admin_id = int(os.getenv("ADMIN_ID"))
ids = [minapova_id, admin_id]


async def send_message(text: str):
    pic_path = get_picture()
    message = get_message(text)
    for each in ids:
    # for each in [admin_id]:  
        fbytes = io.BytesIO(pic_path.read_bytes())  
        file_ = types.InputFile(fbytes, "wazowski.png")
        await bot.send_photo(each, file_, message)
    print("sent!")


async def loop():
    aioschedule.every().day.at("6:00").do(send_message, "доброе утро!")
    aioschedule.every().day.at("11:00").do(send_message, "хорошего дня!")
    aioschedule.every().day.at("16:00").do(send_message, "хорошего вечера!")
    aioschedule.every().day.at("18:00").do(send_message, "доброй ночи!")
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

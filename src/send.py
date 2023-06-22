import asyncio

from main import bot, minapova_id


async def send():
    text = "у меня хорошо"
    await bot.send_message(minapova_id, text)
    
    
if __name__ == "__main__":
    asyncio.run(send())
    
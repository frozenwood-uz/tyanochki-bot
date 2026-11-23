import asyncio
import aiohttp
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message

TOKEN = os.getenv("TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def get_waifu(category: str = "waifu", nsfw: bool = False) -> str | None:
    type_ = "nsfw" if nsfw else "sfw"
    url = f"https://api.waifu.pics/{type_}/{category}"
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data.get("url")
        except Exception as e:
            print(f"Ошибка API: {e}")
    return None

@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Привет! Лови тяночку 💕")
    img_url = await get_waifu("waifu")
    if img_url:
        await message.answer_photo(img_url, caption="Вот твоя тяночка\~")
    else:
        await message.answer("Не удалось загрузить картинку, попробуй ещё раз.")

@dp.message(Command("waifu"))
async def cmd_waifu(message: Message):
    img_url = await get_waifu("waifu")
    if img_url:
        await message.answer_photo(img_url)
    else:
        await message.answer("Ошибка загрузки.")

@dp.message(Command("neko"))
async def cmd_neko(message: Message):
    img_url = await get_waifu("neko")
    if img_url:
        await message.answer_photo(img_url)
    else:
        await message.answer("Ошибка загрузки.")

@dp.message(Command("nsfw"))
async def cmd_nsfw(message: Message):
    img_url = await get_waifu("waifu", nsfw=True)
    if img_url:
        await message.answer_photo(img_url, caption="NSFW 🔥")
    else:
        await message.answer("Ошибка загрузки.")

async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
  

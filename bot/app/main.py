import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from app.handlers import contacts
from config import BOT_TOKEN
from handlers import start, door_selection, faq, photo

# Initialize MemoryStorage
storage = MemoryStorage()

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=storage)

dp.include_router(door_selection.router)
dp.include_router(photo.router)
dp.include_router(faq.router)
dp.include_router(start.router)
dp.include_router(contacts.router)

logging.basicConfig(level=logging.INFO)


async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
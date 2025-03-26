from aiogram import types, Dispatcher, Router
from aiogram.filters import CommandStart

from app.keyboards.main_menu import main_menu_kb

router = Router()

@router.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(
        "Привет! Я помогу подобрать подходящую дверь — входную или межкомнатную.",
        reply_markup=main_menu_kb
    )

# def register_handlers(dp: Dispatcher):
#     dp.message.register(cmd_start, CommandStart())
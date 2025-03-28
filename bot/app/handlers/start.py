from aiogram import types, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from app.keyboards.main_menu import main_menu_kb

router = Router()

@router.message(CommandStart())
async def cmd_start(message: types.Message, state: FSMContext):

    await message.answer(
        "Привет! Я помогу подобрать подходящую дверь — входную или межкомнатную.",
        reply_markup=main_menu_kb
    )
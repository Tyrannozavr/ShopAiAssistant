from aiogram import types, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from app.keyboards.main_menu import main_menu_kb
from app.utils.helpers import UserInteraction

router = Router()

@router.message(CommandStart())
async def cmd_start(message: types.Message, state: FSMContext):
    # Create a new UserInteraction instance
    user_interaction = UserInteraction()

    # Store the UserInteraction instance in FSMContext using the user's telegram_id
    await state.update_data(user_interaction=user_interaction.to_dict())

    await message.answer(
        "Привет! Я помогу подобрать подходящую дверь — входную или межкомнатную.",
        reply_markup=main_menu_kb
    )
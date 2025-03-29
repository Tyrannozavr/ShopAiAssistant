import aiohttp
from aiogram import types, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from app.keyboards.main_menu import main_menu_kb
from app.services.fastapi_client import manager_register  # Mock this function
from logging_config import logger

router = Router()

@router.message(CommandStart())
async def cmd_start(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    text = message.text
    # Check if the start command contains a UTM parameter or manager identifier
    if 'manager_' in text:
        # Extract manager identifier
        manager_identifier = text.split('manager_')[1]
        # Mock the manager_register function call
        response = await manager_register(manager_identifier, chat_id)
        await message.answer(response)
    else:
        if 'utm_' in text:
            # Handle regular user
            city = text.split('utm_')[1]
            # Store city in the user's state
            await state.update_data(city=city)
        
        # Create a personalized greeting
        first_name = message.from_user.first_name or ""
        last_name = message.from_user.last_name or ""
        full_name = f"{first_name} {last_name}".strip()
        greeting = f"Привет, {full_name}! 🌟 Я помогу подобрать подходящую дверь — входную или межкомнатную."
        
        await message.answer(greeting, reply_markup=main_menu_kb)


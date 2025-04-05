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
        greeting = (f"Привет, {full_name}! 🌟 Я помогу подобрать подходящую дверь — входную или межкомнатную. "
                    f"Ты можешь спросить меня о чем угодно или отправить мне фото интерьера / двери, чтобы узнать больше."
                    f"Также я понимаю голосовые")
        
        await message.answer(greeting, reply_markup=main_menu_kb)

@router.message()
async def log_message_details(message: types.Message):
    # Log the message text
    logger.info(f"Message from user: {message.text}")
    message_text = message.text
    file_id = None
    file_type = None

    # Check if the message contains a voice file
    if message.voice:
        file_id = message.voice.file_id
        file_type = "voice"
        # logger.info(f"Received a voice message. File ID: {file_id}, File Type: {file_type}")

    # Check if the message contains a photo
    elif message.photo:
        file_id = message.photo[-1].file_id  # Get the file_id of the highest resolution photo
        file_type = "photo"
        message_text = message.caption or message.text or ""
        # logger.info(f"Received a photo. File ID: {file_id}, File Type: {file_type}")

    # Check if the message contains a document
    elif message.document:
        file_id = message.document.file_id
        file_type = "document"
        # logger.info(f"Received a document. File ID: {file_id}, File Type: {file_type}")
        message_text = message.caption or message.text or ""
    # Log other types of messages
    else:
        logger.info("Received a message with no file attached.")
    logger.info(f"Message text: {message_text}. File ID: {file_id}, File Type: {file_type}")

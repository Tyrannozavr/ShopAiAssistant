from aiogram import types, Router
from aiogram.client.bot import Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import StateFilter

from app.handlers.contacts import InteractionStates
from app.keyboards.interaction import interaction_kb
from app.services.fastapi_client import process_photo
from app.utils.contacts import UserInteractionStates
from logging_config import logger

router = Router()


# @router.message(StateFilter(UserPhotoInteractionStates.waiting_for_photo), lambda message: message.photo or (message.document and message.document.mime_type.startswith('image/')))
@router.message(StateFilter(UserInteractionStates.waiting_for_photo))
async def photo_handler(message: types.Message, state: FSMContext, bot: Bot):
    logger.info(f"Received photo")
    if message.document:
        logger.info(f"{message.document.mime_type}")
    file_id = None
    if message.photo:
        file_id = message.photo[-1].file_id
        await state.update_data(is_photo=True)
    elif message.document:
        file_id = message.document.file_id
        await state.update_data(is_photo=False)
    await state.update_data(file_id=file_id)
    if file_id:
        file_info = await bot.get_file(file_id)
        photo_file = await bot.download_file(file_info.file_path)
        user_data = await state.get_data()
        user_request = message.caption or message.text or ""
        await state.update_data(user_request=user_request)

        # Send a processing message or animation
        processing_message = await message.answer("Обрабатываю ваше фото, пожалуйста, подождите...")

        # Optionally, send an animation (e.g., a loading GIF)
        # You need to have a file_id or URL of the GIF
        # await bot.send_animation(chat_id=message.chat.id, animation='file_id_or_url_of_gif')

        # Process the photo to get advice
        response = await process_photo(photo_file,
                                       user_request=user_request,
                                       door_type=user_data.get('door_type', ''),
                                       priorities=user_data.get('priorities', '') if 'priorities' in user_data else [],
                                       user_id=message.from_user.id)

        # Delete the processing message after receiving the response
        await processing_message.delete()

        await message.answer(response, reply_markup=interaction_kb)
        await state.update_data(gpt_answer=response)
        # After processing the photo, transition to the next step
        await message.answer("Хотите вызвать замерщика?", reply_markup=interaction_kb)
        await state.set_state(InteractionStates.waiting_for_measurer_decision)
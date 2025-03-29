from aiogram import types, Router
from aiogram.client.bot import Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import StateFilter

from app.handlers.contacts import InteractionStates
from app.keyboards.interaction import interaction_kb
from app.services.fastapi_client import process_photo

router = Router()

# Define states
class UserPhotoInteractionStates(StatesGroup):
    waiting_for_photo = State()

@router.message(StateFilter(UserPhotoInteractionStates.waiting_for_photo), lambda message: message.photo or (message.document and message.document.mime_type.startswith('image/')))
async def photo_handler(message: types.Message, state: FSMContext, bot: Bot):
    file_id = None

    if message.photo:
        file_id = message.photo[-1].file_id
    elif message.document:
        file_id = message.document.file_id

    if file_id:
        file_info = await bot.get_file(file_id)
        photo_file = await bot.download_file(file_info.file_path)
        user_data = await state.get_data()
        user_request = message.caption or message.text or ""

        # Process the photo to get advice
        response = await process_photo(photo_file,
                                     user_request=user_request,
                                     door_type=user_data.get('door_type', ''),
                                     priorities=user_data.get('priorities', '') if 'priorities' in user_data else [])  # Extract priorities from the state if available, otherwise use an empty list)
        await message.answer(response, reply_markup=interaction_kb)
        # After processing the photo, transition to the next step
        await message.answer("Хотите вызвать замерщика?", reply_markup=interaction_kb)
        await state.set_state(InteractionStates.waiting_for_measurer_decision)
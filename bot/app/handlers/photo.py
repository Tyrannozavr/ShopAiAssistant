from aiogram import types, Router
from aiogram.client.bot import Bot
from aiogram.fsm.context import FSMContext
from app.services.fastapi_client import process_photo

router = Router()

@router.message(lambda message: message.photo or (message.document and message.document.mime_type.startswith('image/')))
async def photo_handler(message: types.Message, state: FSMContext, bot: Bot):
    file_id = None

    if message.photo:
        file_id = message.photo[-1].file_id
    elif message.document:
        file_id = message.document.file_id

    if file_id:
        file_info = await bot.get_file(file_id)
        photo_file = await bot.download_file(file_info.file_path)

        # Process the photo to get advice
        advice = await process_photo(photo_file)

        # Retrieve user interaction data from the state
        user_data = await state.get_data()
        user_interaction = {
            'door_type': user_data.get('door_type', ''),
            'priorities': user_data.get('priorities', []),
            'photo': file_id,
            'gpt_answer': advice,
            'contact': user_data.get('contact', ''),
            'address': user_data.get('address', '')
        }

        # Send the user interaction data and advice as a response
        response_message = (
            f"Тип: {user_interaction['door_type']}\n"
            f"Приоритеты: {', '.join(user_interaction['priorities'])}\n"
            f"Фото: [ссылка]\n"
            f"GPT-ответ: {user_interaction['gpt_answer']}\n"
            f"Контакт: {user_interaction['contact']}\n"
            f"Адрес: {user_interaction['address']}"
        )
        await message.answer(response_message)

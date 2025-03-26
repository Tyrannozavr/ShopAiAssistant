from aiogram import types, Router
from aiogram.client.bot import Bot

from app.services.fastapi_client import process_photo

router = Router()

# @router.message(content_types=[types.ContentType.PHOTO, types.ContentType.DOCUMENT])
@router.message(lambda message: message.photo or message.document and message.document.mime_type.startswith('image/'))
async def photo_handler(message: types.Message, bot: Bot):
    file_id = None

    if message.photo:
        # Handle photo
        file_id = message.photo[-1].file_id
    elif message.document:
        # Handle document with image MIME type
        file_id = message.document.file_id

    if file_id:
        # Get the file information
        file_info = await bot.get_file(file_id)
        # Download the file
        photo_file = await bot.download_file(file_info.file_path)
        advice = await process_photo(photo_file)
        await message.answer(advice)

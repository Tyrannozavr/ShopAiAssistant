from aiogram import types, Dispatcher, Router
from app.services.gpt_client import get_gpt_response


router = Router()

@router.message(lambda message: message.text == "Задать вопрос")
async def faq_handler(message: types.Message):
    response = await get_gpt_response(message.text)
    await message.answer(response)


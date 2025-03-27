from aiogram import types, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import StateFilter
from app.services.fastapi_client import process_question

router = Router()

# Define states
class FAQStates(StatesGroup):
    waiting_for_question = State()

@router.callback_query(lambda c: c.data == 'FAQ')
async def faq_handler(callback_query: CallbackQuery, state: FSMContext):
    # Set the state to waiting for a question
    await state.set_state(FAQStates.waiting_for_question)
    
    # Prompt the user to enter their question
    await callback_query.message.answer("Пожалуйста, введите ваш вопрос:")
    await callback_query.answer()

@router.message(StateFilter(FAQStates.waiting_for_question))
async def process_faq_question(message: types.Message, state: FSMContext):
    # Extract the question from the message
    question = message.text.strip()

    # Process the question to get an answer
    answer = await process_question(question)

    # Retrieve user interaction data from the state
    user_data = await state.get_data()
    user_interaction = {
        'door_type': user_data.get('door_type', ''),
        'priorities': user_data.get('priorities', []),
        'photo': user_data.get('photo', ''),
        'gpt_answer': answer,
        'contact': user_data.get('contact', ''),
        'address': user_data.get('address', '')
    }

    # Send the user interaction data and answer as a response
    response_message = (
        f"Тип: {user_interaction['door_type']}\n"
        f"Приоритеты: {', '.join(user_interaction['priorities'])}\n"
        f"Фото: {user_interaction['photo']}\n"
        f"GPT-ответ: {user_interaction['gpt_answer']}\n"
        f"Контакт: {user_interaction['contact']}\n"
        f"Адрес: {user_interaction['address']}\n"
        f"Вопрос пользователя: {question}\n"
    )
    await message.answer(response_message)

    # Reset the state
    await state.clear()
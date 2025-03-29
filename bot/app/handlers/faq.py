from aiogram import types, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import StateFilter

from app.handlers.contacts import InteractionStates
from app.keyboards.interaction import interaction_kb
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
    await state.update_data(user_request=question)

    # Process the question to get an answer

    # Retrieve user interaction data from the state
    user_data = await state.get_data()
    processing_message = await message.answer("Обрабатываю ваш вопрос, пожалуйста, подождите...")

    response = await process_question(door_type=user_data.get('door_type', ''),
                                priorities=user_data.get('priorities', []),
                                user_request=question,
                                user_id=message.from_user.id)
    await processing_message.delete()
    await state.update_data(gpt_answer=response)

    await message.answer(response)

    # After processing the FAQ, transition to the next step
    await message.answer("Хотите вызвать замерщика?", reply_markup=interaction_kb)
    await state.set_state(InteractionStates.waiting_for_measurer_decision)
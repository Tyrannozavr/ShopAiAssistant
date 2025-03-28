import logging
from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import StateFilter
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

router = Router()

# Define states
class InteractionStates(StatesGroup):
    waiting_for_measurer_decision = State()
    waiting_for_contact = State()
    waiting_for_address = State()

# Define the interaction keyboard
interaction_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Да, вызвать замерщика")],
        [KeyboardButton(text="Пока нет")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

@router.message(StateFilter(InteractionStates.waiting_for_measurer_decision))
async def handle_measurer_decision(message: types.Message, state: FSMContext):
    logging.info(f"Received message: {message.text} in state: {await state.get_state()}")
    if message.text == "Да, вызвать замерщика":
        await message.answer("Пожалуйста, отправьте ваш номер телефона или контакт через кнопку.")
        await state.set_state(InteractionStates.waiting_for_contact)
    elif message.text == "Пока нет":
        await message.answer("Если передумаете, просто дайте знать!")
        await state.clear()

@router.message(StateFilter(InteractionStates.waiting_for_contact))
async def handle_contact(message: types.Message, state: FSMContext):
    logging.info(f"Received contact: {message.text} in state: {await state.get_state()}")
    contact = message.text
    await state.update_data(contact=contact)
    await message.answer("Пожалуйста, укажите город, улицу и дом для расчёта доставки и монтажа.")
    await state.set_state(InteractionStates.waiting_for_address)

@router.message(StateFilter(InteractionStates.waiting_for_address))
async def handle_address(message: types.Message, state: FSMContext):
    logging.info(f"Received address: {message.text} in state: {await state.get_state()}")
    address = message.text
    await state.update_data(address=address)
    await message.answer("Спасибо! Менеджер скоро свяжется с вами.")
    await state.clear()
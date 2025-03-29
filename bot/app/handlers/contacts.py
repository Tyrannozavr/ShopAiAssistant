import logging

from aiogram import types, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

from app.handlers.door_selection import UserInteractionStates
from app.utils.contacts import start_contact_interaction
from logging_config import logger

router = Router()

# Define states
class InteractionStates(StatesGroup):
    waiting_for_measurer_decision = State()
    waiting_for_contact = State()
    waiting_for_address = State()
    waiting_for_manual_input = State()  # New state for manual input

@router.message(StateFilter(InteractionStates.waiting_for_measurer_decision))
async def handle_measurer_decision(message: types.Message, state: FSMContext):
    if message.text == "Да, вызвать замерщика":
        await state.update_data(call_measurer=True)
    elif message.text == "Пока нет":
        await state.update_data(call_measurer=False)
    await start_contact_interaction(message, state)

@router.message(StateFilter(UserInteractionStates.waiting_for_contact))
async def handle_contact_input(message: Message, state: FSMContext):
    if message.contact:
        # If the user shared their contact, use it
        contact_info = f"Телефон: {message.contact.phone_number}"
        # Save the contact information in the state
        await state.update_data(contact=contact_info)
        await message.answer("Спасибо! Ваши контактные данные сохранены.")
    elif message.text == "✏️ Ввести вручную":
        # Transition to the manual input state
        await message.answer("Пожалуйста, введите ваши контактные данные вручную.")
        await state.set_state(InteractionStates.waiting_for_manual_input)
        return  # Exit the function to wait for manual input
    else:
        # Otherwise, assume manual input
        contact_info = message.text
        # Save the contact information in the state
        await state.update_data(contact=contact_info)
        await message.answer("Спасибо! Ваши контактные данные сохранены.")

    # Ask for address details
    await message.answer("Пожалуйста, укажите город, улицу и дом для расчёта доставки и монтажа.")
    await state.set_state(InteractionStates.waiting_for_address)

@router.message(StateFilter(InteractionStates.waiting_for_manual_input))
async def handle_manual_input(message: Message, state: FSMContext):
    # Assume the message text is the manual input
    contact_info = message.text
    # Return to handle_contact_input with the manual input
    await state.update_data(contact=contact_info)
    await handle_contact_input(message, state)

from app.services.fastapi_client import save_order

@router.message(StateFilter(InteractionStates.waiting_for_address))
async def handle_address(message: types.Message, state: FSMContext):
    logging.info(f"Received address: {message.text} in state: {await state.get_state()}")
    address = message.text
    await state.update_data(address=address)
    await message.answer("Спасибо! Менеджер скоро свяжется с вами.")
    
    # Retrieve all data from the state
    order_data = await state.get_data()
    
    # Save the order
    await save_order(order_data)
    await state.clear()
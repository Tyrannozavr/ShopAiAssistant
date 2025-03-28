from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from app.keyboards.interaction import contact_kb

class UserInteractionStates(StatesGroup):
    waiting_for_door_type = State()
    waiting_for_priorities = State()
    waiting_for_photo_decision = State()
    waiting_for_contact = State()
    waiting_for_photo = State()

async def start_contact_interaction(message: types.Message, state: FSMContext):
    # Prepare default contact data
    user_data = message.from_user
    default_contact = {
        'username': f"@{user_data.username}" if user_data.username else None,
        'phone_number': None,  # Telegram doesn't provide phone number directly
        'first_name': user_data.first_name or None,
        'last_name': user_data.last_name or None
    }

    # Store the contact data in the state
    await state.update_data(contact=default_contact)

    # Create a message with the available contact data
    contact_info = "Пожалуйста, предоставьте ваши контактные данные:\n"
    if default_contact['first_name']:
        contact_info += f"Имя: {default_contact['first_name']}\n"
    if default_contact['last_name']:
        contact_info += f"Фамилия: {default_contact['last_name']}\n"
    if default_contact['username']:
        contact_info += f"Username: {default_contact['username']}\n"
    if default_contact['phone_number']:
        contact_info += f"Телефон: {default_contact['phone_number']}\n"

    contact_info += "\nВы можете отправить свой номер телефона или ввести данные вручную."
    await state.update_data(default_contact=default_contact)

    # Send a message with the contact data and options
    await message.answer(contact_info, reply_markup=contact_kb)

    # Transition to a state where the user can provide contact information
    await state.set_state(UserInteractionStates.waiting_for_contact)
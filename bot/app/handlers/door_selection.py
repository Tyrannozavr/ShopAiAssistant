from aiogram import types
from aiogram.dispatcher.router import Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from app.keyboards.priorities import create_priorities_kb
from app.keyboards.interaction import interaction_kb

# Define states
class UserInteractionStates(StatesGroup):
    waiting_for_door_type = State()
    waiting_for_priorities = State()

# Declare a new router
router = Router()

@router.message(lambda message: message.text in ["Входная дверь", "Межкомнатная дверь"])
async def door_selection(message: types.Message, state: FSMContext):
    # Save the door type in the user's state
    await state.update_data(door_type=message.text)
    
    # Transition to the next state
    await state.set_state(UserInteractionStates.waiting_for_priorities)
    await state.update_data(priorities=[])
    await message.answer(
        "Что для тебя главное в двери? выбери до 3 пунктов",
        reply_markup=create_priorities_kb([])
    )

@router.callback_query(lambda c: c.data.startswith('priority:'))
async def handle_priority_selection(callback_query: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    selected_priority = callback_query.data.split(':')[1]
    priorities = user_data.get('priorities', [])

    if selected_priority in priorities:
        priorities.remove(selected_priority)
    elif len(priorities) < 3:
        priorities.append(selected_priority)
    else:
        await callback_query.answer("Вы можете выбрать только 3 приоритета.", show_alert=True)
        return

    # Save the updated priorities in the user's state
    await state.update_data(priorities=priorities)

    # Only update the message if there is a change
    await callback_query.message.edit_reply_markup(
        reply_markup=create_priorities_kb(priorities)
    )
    await callback_query.answer()

@router.callback_query(lambda c: c.data == 'continue')
async def handle_continue(callback_query: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    priorities = user_data.get('priorities', [])
    if len(priorities) == 0:
        await callback_query.answer("Выберите хотя бы один приоритет.", show_alert=True)
    else:
        await callback_query.message.answer(
            "Отлично, теперь вы можете отправить мне фото и я помогу вам определиться с выбором. "
            "Либо вы можете заказать вызов замерщика на дом.",
            reply_markup=interaction_kb
        )

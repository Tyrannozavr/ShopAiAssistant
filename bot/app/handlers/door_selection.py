from aiogram import types
from aiogram.dispatcher.router import Router
from aiogram.types import Message, CallbackQuery

from app.keyboards.priorities import create_priorities_kb

# Dictionary to store user priorities
user_priorities = {}

# Declare a new router
router = Router()

@router.message(lambda message: message.text == "Входная дверь" or message.text == "Межкомнатная дверь")
async def door_selection(message: types.Message):
    user_id = message.from_user.id
    user_priorities[user_id] = []
    await message.answer(
        "Выберите ваши приоритеты (можно выбрать до 3):",
        reply_markup=create_priorities_kb(user_priorities[user_id])
    )

@router.callback_query(lambda c: c.data.startswith('priority:'))
async def handle_priority_selection(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    selected_priority = callback_query.data.split(':')[1]

    if selected_priority in user_priorities[user_id]:
        user_priorities[user_id].remove(selected_priority)
    elif len(user_priorities[user_id]) < 3:
        user_priorities[user_id].append(selected_priority)
    else:
        await callback_query.answer("Вы можете выбрать только 3 приоритета.", show_alert=True)
        return

    # Only update the message if there is a change
    await callback_query.message.edit_reply_markup(
        reply_markup=create_priorities_kb(user_priorities[user_id])
    )
    await callback_query.answer()

@router.callback_query(lambda c: c.data == 'continue')
async def handle_continue(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    if len(user_priorities[user_id]) == 0:
        await callback_query.answer("Выберите хотя бы один приоритет.", show_alert=True)
    else:
        await callback_query.message.answer(f"Вы выбрали: {', '.join(user_priorities[user_id])}")
        # Proceed with the next step in your bot's flow
        await callback_query.answer()

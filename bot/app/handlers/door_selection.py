from aiogram import types, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove

from app.keyboards.photo_options import photo_options_kb
from app.keyboards.priorities import create_priorities_kb
from app.utils.contacts import start_contact_interaction, UserInteractionStates
from logging_config import logger

# Declare a new router
router = Router()

@router.message(lambda message: message.text in ["Входная дверь", "Межкомнатная дверь"])
async def door_selection(message: Message, state: FSMContext):
    # Save the door type in the user's state
    await state.update_data(door_type=message.text)

    # Transition to the next state
    await state.set_state(UserInteractionStates.waiting_for_priorities)
    await state.update_data(priorities=[])
    await message.answer(
        "Выберите ваши приоритеты (можно выбрать до 3):",
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
        # Transition to the next state
        await state.set_state(UserInteractionStates.waiting_for_photo_decision)
        await callback_query.message.answer(
            "Хочешь, проанализирую твой интерьер и предложу, что подойдёт под него? "
            "Можно прислать фото помещения или двери, которая нравится — подскажу, в каком стиле двигаться.",
            reply_markup=photo_options_kb
        )

@router.message(StateFilter(UserInteractionStates.waiting_for_photo_decision))
async def handle_photo_decision(message: types.Message, state: FSMContext):
    logger.info(f"Received photo decision: {message.text}")
    if message.text == "📸 Прислать фото интерьера / двери":
        await message.answer("Хорошо, тогда жду фото. (к фото вы можете добавить любой интересующий вас вопрос)",
                             reply_markup=ReplyKeyboardRemove())
        await state.set_state(UserInteractionStates.waiting_for_photo)
        logger.info(f"Waiting for photo in state: {await state.get_state()}")
    elif message.text == "🙈 Пока без фото":
        await start_contact_interaction(message, state)
    else:
        logger.error(f"Invalid photo decision: {message.text}")






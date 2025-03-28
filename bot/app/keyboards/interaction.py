
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Define the interaction keyboard with options to call a measurer or not
interaction_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Да, вызвать замерщика")],
        [KeyboardButton(text="Пока нет")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
contact_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📞 Отправить номер телефона", request_contact=True)],
        [KeyboardButton(text="✏️ Ввести вручную")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

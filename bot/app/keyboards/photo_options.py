from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Define the photo options keyboard
photo_options_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📸 Прислать фото интерьера / двери")],
        [KeyboardButton(text="🙈 Пока без фото")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
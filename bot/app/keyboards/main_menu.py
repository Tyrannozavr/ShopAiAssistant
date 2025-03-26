from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Define the main menu keyboard with button rows
main_menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Входная дверь")],
        [KeyboardButton(text="Межкомнатная дверь")],
        [KeyboardButton(text="Позвоните мне")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
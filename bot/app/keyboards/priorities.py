from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def create_priorities_kb(selected_priorities):
    buttons = [
        InlineKeyboardButton(
            text=f"{'✅ ' if 'Взломостойкость' in selected_priorities else ''}Взломостойкость",
            callback_data='priority:Взломостойкость'
        ),
        InlineKeyboardButton(
            text=f"{'✅ ' if 'Утепление / улица' in selected_priorities else ''}Утепление / улица",
            callback_data='priority:Утепление / улица'
        ),
        InlineKeyboardButton(
            text=f"{'✅ ' if 'Электронный замок' in selected_priorities else ''}Электронный замок",
            callback_data='priority:Электронный замок'
        ),
        InlineKeyboardButton(
            text=f"{'✅ ' if 'Внешний вид' in selected_priorities else ''}Внешний вид",
            callback_data='priority:Внешний вид'
        ),
        InlineKeyboardButton(
            text=f"{'✅ ' if 'Бюджет' in selected_priorities else ''}Бюджет",
            callback_data='priority:Бюджет'
        ),
        InlineKeyboardButton(
            text="Задать вопрос",
            callback_data='FAQ'
        ),
        InlineKeyboardButton(
            text="Продолжить",
            callback_data='continue'
        )
    ]
    return InlineKeyboardMarkup(inline_keyboard=[buttons[i:i + 2] for i in range(0, len(buttons), 2)])

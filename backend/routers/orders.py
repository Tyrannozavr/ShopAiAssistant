from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get("/")
async def get_orders():
    # Mocked response for getting orders
    return {"orders": [{"id": 1, "item": "Door", "quantity": 2}]}

@router.post("/")
async def create_order(order: dict):
    """
2025-03-29 14:47:51,910 - logging_config - INFO - {'city': 'Astrahan', 'door_type': 'Входная дверь', 'priorities': ['Внешний вид', 'Электронный замок'], 'contact': 'Телефон: +375336390687', 'default_contact': {'username': '@tyrannozavr', 'phone_number': None, 'first_name': 'Дмитрий', 'last_name': 'Счислёнок'}, 'address': 'fdsfs'}
2025-03-29 18:10:43,470 - logging_config - INFO - {'city': 'astrahan', 'door_type': 'Входная дверь', 'priorities': ['Взломостойкость', 'Утепление / улица', 'Внешний вид'], 'contact': 'Телефон: +375336390687', 'default_contact': {'username': '@tyrannozavr', 'phone_number': None, 'first_name': 'Дмитрий', 'last_name': 'Счислёнок'}, 'address': 'yy yyu'}
2025-03-29 18:17:29,248 - logging_config - INFO - {'city': 'astrahan', 'door_type': 'Межкомнатная дверь', 'priorities': ['Взломостойкость', 'Электронный замок'], 'user_request': 'мне нужен совет', 'gpt_answer': 'Answer for the given question', 'call_measurer': False, 'contact': 'апвапв', 'default_contact': {'username': '@tyrannozavr', 'phone_number': None, 'first_name': 'Дмитрий', 'last_name': 'Счислёнок'}, 'address': 'ррро ооо'}
Тип: Входная
Приоритеты: Утепление, Электронный замок
Фото: [ссылка]
GPT-ответ: “На фото холодный подъезд — стоит взять дверь с терморазрывом...”
Контакт: @username / +7 999 000-00-00
Адрес: Казань, ул. Баумана, 18
Время: [время]
"""
    # Mocked response for creating an order
    if not order:
        raise HTTPException(status_code=400, detail="Invalid order data")
    return {"message": "Order created successfully", "order": order}
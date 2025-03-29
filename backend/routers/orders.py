from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get("/")
async def get_orders():
    # Mocked response for getting orders
    return {"orders": [{"id": 1, "item": "Door", "quantity": 2}]}

@router.post("/")
async def create_order(order: dict):
    """2025-03-29 14:47:51,910 - logging_config - INFO - All state data: {'city': 'Astrahan', 'door_type': 'Входная дверь', 'priorities': ['Внешний вид', 'Электронный замок'], 'contact': 'Телефон: +375336390687', 'default_contact': {'username': '@tyrannozavr', 'phone_number': None, 'first_name': 'Дмитрий', 'last_name': 'Счислёнок'}, 'address': 'fdsfs'}
"""
    # Mocked response for creating an order
    if not order:
        raise HTTPException(status_code=400, detail="Invalid order data")
    return {"message": "Order created successfully", "order": order}
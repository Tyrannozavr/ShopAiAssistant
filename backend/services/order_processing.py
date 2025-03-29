from sqlalchemy.orm import Session
from schemas.order import Order as OrderSchema
from core.logging_config import logger
from models import Manager, City, Order
from services.telegram_notification import TelegramNotificationService
from datetime import datetime

def select_manager_for_order(order: OrderSchema, db: Session) -> str:
    # Try to find a manager with the same city and is_staff=True
    manager = db.query(Manager).join(City).filter(
        City.name == order.city,
        Manager.is_staff == True,
        Manager.chat_id.isnot(None)
    ).first()

    if manager:
        logger.info(f"Selected manager {manager.username} for city {order.city}")
        return manager.chat_id

    # If no manager found, try to find a manager without a city
    manager = db.query(Manager).filter(
        Manager.city_id.is_(None),
        Manager.is_staff == True,
        Manager.chat_id.isnot(None)
    ).first()

    if manager:
        logger.info(f"Selected manager {manager.username} without specific city")
        return manager.chat_id

    # Log an error if no suitable manager is found
    logger.error("No appropriate manager found for the order")
    return None

def generate_order_message(order: OrderSchema) -> str:
    # Generate a formatted message from the order details
    message = (
        f"Тип: {order.door_type}\n"
        f"Город: {order.city}\n"
        f"Приоритеты: {', '.join(order.priorities)}\n"
        f"GPT-ответ: {order.gpt_answer or 'N/A'}\n"
        f"Контакт: {order.default_contact.username or 'N/A'} / {order.contact}\n"
        f"Адрес: {order.address}\n"
        f"Время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"Вызвать замерщика: {"да" if order.call_measurer else "нет"}\n"
    )
    return message

def send_order_notification(chat_id: str, message: str, file_id: str = None):
    # Send the order message using TelegramNotificationService
    notification_service = TelegramNotificationService()
    notification_service.send_message(chat_id=chat_id, message=message, file_id=file_id)

def process_order(order: OrderSchema, db: Session):
    # Store the order in the database
    order_record = Order(
        city=order.city,
        door_type=order.door_type,
        priorities=", ".join(order.priorities),
        contact=order.contact,
        username=order.default_contact.username,
        phone_number=order.default_contact.phone_number,
        first_name=order.default_contact.first_name,
        last_name=order.default_contact.last_name,
        address=order.address,
        user_request=order.user_request,
        gpt_answer=order.gpt_answer,
        call_measurer=order.call_measurer,
        file_id=order.file_id
    )
    db.add(order_record)
    db.commit()

    # Select a manager for the order
    chat_id = select_manager_for_order(order, db)

    # Generate the order message
    order_message = generate_order_message(order)

    logger.info(f"Generated order message for chat_id {chat_id}: {order_message}")
    if chat_id:
        send_order_notification(chat_id=chat_id, message=order_message, file_id=order.file_id)

    # Add more detailed processing logic here

    return {"status": "success", "message": "Order processed successfully", "chat_id": chat_id}
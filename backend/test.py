import asyncio
from dotenv import load_dotenv
from services.telegram_notification import TelegramNotificationService

load_dotenv()

async def main():
    notification_service = TelegramNotificationService()
    await notification_service.send_message(chat_id="972834722",
                                            file_id="AgACAgIAAxkBAAMHZ-ifxedoiq88BQYwqP3ZagVnXAsAArDnMRuZb0hL6ueSVuFymeEBAAMCAAN5AAM2BA",
                                            message="Hello, this is a test message!")
    # await notification_service.send_message(chat_id="972834722", message="Hello, this is a test message!")

if __name__ == "__main__":
    asyncio.run(main())
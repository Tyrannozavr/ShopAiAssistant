import os
from telegram import Bot
from telegram.error import TelegramError
from core.logging_config import logger

class TelegramNotificationService:
    def __init__(self):
        self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN")  # Ensure you have this token in your environment variables
        if not self.bot_token:
            raise ValueError("Telegram bot token is not set in environment variables.")
        self.bot = Bot(token=self.bot_token)

    def send_message(self, chat_id: str, message: str, file_id: str = None):
        try:
            if file_id:
                # Send the file if file_id is provided
                self.bot.send_document(chat_id=chat_id, document=file_id, caption=message)
                logger.info(f"File sent to chat_id {chat_id} with file_id {file_id}: {message}")
            else:
                # Send a text message if no file_id is provided
                self.bot.send_message(chat_id=chat_id, text=message)
                logger.info(f"Message sent to chat_id {chat_id}: {message}")
        except TelegramError as e:
            logger.error(f"Failed to send message to chat_id {chat_id}: {e}")

# Example usage
# if __name__ == "__main__":
#     service = TelegramNotificationService()
#     service.send_message(chat_id="123456789", message="Hello, this is a test message!")
#     service.send_message(chat_id="123456789", message="Here is your document.", file_id="your_file_id_here")
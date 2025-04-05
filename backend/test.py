import asyncio
from dotenv import load_dotenv

from core.Config import settings
from depends.db import get_db
from services.interaction_service import InteractionService

load_dotenv()

async def main():
    # Initialize the service
    session = next(get_db())
    interaction_service = InteractionService(db=session, api_key=settings.openai_key, base_url=settings.openai_url)

    # Start or continue an interaction
    response_data = interaction_service.start_interaction(user_id="user_telegram_id",
                                                          user_message="Хочу дверь из железа")

    print("Response:", response_data["response"])
    print(2, response_data["contact_data"])
    print(3, response_data["summary"])
if __name__ == "__main__":
    asyncio.run(main())
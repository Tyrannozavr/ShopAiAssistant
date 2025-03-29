from io import BytesIO

from PIL import Image
from dotenv import load_dotenv

from depends.db import get_db
from services.chatgpt import ChatGPT


# Set up the database session (replace with your actual database URL)
# DATABASE_URL = "sqlite:///test.db"  # Example using SQLite
# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
load_dotenv(".env")
def test_process_photo():
    # Initialize the ChatGPT service
    chatgpt_service = ChatGPT()

    # Create a test database session
    # db = SessionLocal()
    db = next(get_db())
    # Create a simple test image in memory
    image = Image.new('RGB', (1024, 1024), color = 'red')
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    buffered.seek(0)

    # Define test parameters
    door_type = "wooden"
    priorities = ["security", "aesthetics"]
    user_request = "Я хочу какую нибудь классную дверь для гостиной."

    # Call the process_photo method
    try:
        result = chatgpt_service.process_photo(buffered, door_type, priorities, user_request, db)
        print("Test Result:", result)
    except Exception as e:
        print("Test Failed:", str(e))

if __name__ == "__main__":
    test_process_photo()
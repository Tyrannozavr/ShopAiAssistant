import unittest
import asyncio
from app.services.fastapi_client import process_photo

class TestFastAPIClient(unittest.IsolatedAsyncioTestCase):

    async def test_process_photo_real(self):
        # Test data
        with open('/home/user/Изображения/дверь.jpg', 'rb') as photo_file:
            door_type = "межкомнатная"
            priorities = ["красота", "стоимость", "полезность"]
            user_request = "Хочу заменить это дверь"

            # Call the function
            response = await process_photo(photo_file, door_type, priorities, user_request, user_id=123456)

            # Print the response
            print("Response from process_photo:", response)

            # Basic assertion to ensure we get a response
            self.assertIsInstance(response, str)
            self.assertTrue(len(response) > 0)

if __name__ == '__main__':
    unittest.main()
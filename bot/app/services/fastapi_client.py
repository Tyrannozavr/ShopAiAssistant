import aiohttp
from app.config import BACKEND_URL

async def process_photo(photo_file):
    return "Advice for the given photo"  # TODO: Implement the logic to process the photo and return advice
    # async with aiohttp.ClientSession() as session:
    #     async with session.post(f"{FASTAPI_URL}/process_photo", data={"photo": photo_file}) as response:
    #         return await response.text()


async def process_question(question):
    return "Answer for the given question"  # TODO: Implement the logic to process the question and return answer
    # async with aiohttp.ClientSession() as session:
    #     async with session.post(f"{FASTAPI_URL}/process_question", data={"question": question}) as response:
    #         return await response.text()


import aiohttp
from app.config import BACKEND_URL  # Ensure BACKEND_URL is defined in your config

async def manager_register(identifier, chat_id):
    url = f"{BACKEND_URL}/manager"
    data = {
        "identifier": identifier,
        "chat_id": chat_id
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, json=data) as response:
                if response.status == 200:
                    result = await response.json()
                    return f"Manager registered successfully: {result.get('message', 'Success')}"
                else:
                    return f"Failed to register manager. Status code: {response.status}"
        except aiohttp.ClientError as e:
            return f"Error connecting to the registration service: {str(e)}"
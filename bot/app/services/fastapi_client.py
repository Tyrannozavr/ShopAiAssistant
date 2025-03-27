import aiohttp
from app.config import FASTAPI_URL

async def process_photo(photo_file):
    return "Advice for the given photo"  # TODO: Implement the logic to process the photo and return advice
    # async with aiohttp.ClientSession() as session:
    #     async with session.post(f"{FASTAPI_URL}/process_photo", data={"photo": photo_file}) as response:
    #         return await response.text()


async def process_question(question):
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{FASTAPI_URL}/process_question", data={"question": question}) as response:
            return await response.text()
import aiohttp
from app.config import FASTAPI_URL

async def process_photo(photo_file):
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{FASTAPI_URL}/process_photo", data={"photo": photo_file}) as response:
            return await response.text()
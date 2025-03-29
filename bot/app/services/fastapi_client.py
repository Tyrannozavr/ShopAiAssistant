from typing import BinaryIO

import aiohttp
from aiohttp import FormData, ClientResponse

from app.config import BACKEND_URL


async def process_photo(photo_file: BinaryIO | None, door_type: str, priorities: list, user_request: str) -> str:
    url = f"{BACKEND_URL}/api/chatgpt/photo"
    
    # Create a FormData object to handle file uploads
    form_data = FormData()
    form_data.add_field('door_type', door_type)
    form_data.add_field('priorities', ','.join(priorities))
    form_data.add_field('user_request', user_request)
    
    if photo_file:
        form_data.add_field('photo', photo_file, filename='photo.jpg', content_type='image/jpeg')
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, data=form_data) as response:
                if response.status == 200:
                    return await response.text()
                else:
                    return f"Failed to process photo. Status code: {response.status}"
        except aiohttp.ClientError as e:
            return f"Error connecting to the photo processing service: {str(e)}"


async def process_question(question) -> ClientResponse:
    return "Answer for the given question"  # TODO: Implement the logic to process the question and return answer
    # async with aiohttp.ClientSession() as session:
    #     async with session.post(f"{FASTAPI_URL}/process_question", data={"question": question}) as response:
    #         return await response.text()



async def manager_register(identifier, chat_id) -> ClientResponse:
    url = f"{BACKEND_URL}/api/manager/register_chat"
    data = {
        "identifier": identifier,
        "chat_id": str(chat_id)
    }
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, json=data) as response:
                if response.status == 200:
                    result = await response.json()
                    return result.get('message', 'Success')
                else:
                    return f"Failed to register manager. Status code: {response.status}"
        except aiohttp.ClientError as e:
            return f"Error connecting to the registration service: {str(e)}"
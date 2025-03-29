from typing import BinaryIO

import aiohttp
from aiohttp import FormData, ClientResponse

from app.config import BACKEND_URL
from logging_config import logger


async def process_photo(photo_file: BinaryIO | None, door_type: str, priorities: list, user_request: str, user_id: int) -> str:
    url = f"{BACKEND_URL}/api/chatgpt/photo"
    
    # Create a FormData object to handle file uploads
    form_data = FormData()
    form_data.add_field('door_type', door_type)
    form_data.add_field('priorities', ','.join(priorities))
    form_data.add_field('user_request', user_request)
    form_data.add_field('user_id', str(user_id))
    
    if photo_file:
        form_data.add_field('photo', photo_file, filename='photo.jpg', content_type='image/jpeg')
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, data=form_data) as response:
                if response.status == 200:
                    response = await response.json()
                    return response.get("result")
                else:
                    error = await response.json()
                    logger.error(f"Failed to process question. Status code: {response.status}, error: {error}")
                    return f"Failed to process йгуыешщт. Status code: {response.status}"
        except aiohttp.ClientError as e:
            return f"Error connecting to the photo processing service: {str(e)}"


async def process_question(door_type: str, priorities: list, user_request: str, user_id: int) -> str:
    url = f"{BACKEND_URL}/api/chatgpt/question"

    # Prepare the data as a JSON payload
    json_data = {
        'door_type': door_type,
        'priorities': priorities,
        'user_request': user_request,
        'user_id': user_id
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, json=json_data) as response:
                if response.status == 200:
                    response = await response.json()
                    return response.get("result")
                else:
                    error = await response.json()
                    logger.error(f"Failed to process question. Status code: {response.status}, error: {error}")
                    return f"Failed to process question. Status code: {response.status}"
        except aiohttp.ClientError as e:
            return f"Error connecting to the question processing service: {str(e)}"


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

async def save_order(order_data: dict) -> str:
    logger.info(f"Order data: {order_data}")
    url = f"{BACKEND_URL}/api/orders/"
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, json=order_data) as response:
                if response.status == 200:
                    result = await response.json()
                    return result.get('message', 'Order saved successfully')
                else:
                    return f"Failed to save order. Status code: {response.status}"
        except aiohttp.ClientError as e:
            return f"Error connecting to the order service: {str(e)}"

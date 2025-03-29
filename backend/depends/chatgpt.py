from services.chatgpt import ChatGPT
from services.chatgptvision import ChatGPTVision


def get_chatgpt_vision_service():
    return ChatGPTVision()

def get_chatgpt_service():
    return ChatGPT()  # Placeholder for actual implementation

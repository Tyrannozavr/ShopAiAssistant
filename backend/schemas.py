from pydantic import BaseModel

class TokenData(BaseModel):
    user_id: int
    identifier: str
    username: str
    city: str
    is_staff: bool
    is_admin: bool
    chat_id: str
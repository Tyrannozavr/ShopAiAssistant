from pydantic import BaseModel, Field
from typing import List, Optional

class Contact(BaseModel):
    username: Optional[str] = None
    phone_number: Optional[str] = None
    first_name: str
    last_name: Optional[str] = None

class Order(BaseModel):
    city: str
    door_type: str
    priorities: List[str] = Field(default_factory=list)
    contact: str
    default_contact: Contact
    address: str
    user_request: Optional[str] = None
    gpt_answer: Optional[str] = None
    call_measurer: Optional[bool] = False
    file_id: Optional[str] = None,
    is_photo: Optional[bool] = True,

    class Config:
        json_schema_extra = {
            "example": {
                "city": "Astrahan",
                "door_type": "Входная дверь",
                "priorities": ["Внешний вид", "Электронный замок"],
                "contact": "Телефон: +1111111",
                "default_contact": {
                    "username": "@tyrannozavr",
                    "phone_number": None,
                    "first_name": "Дмитрий",
                    "last_name": "Счислёнок"
                },
                "address": "fdsfs",
                "user_request": "мне нужен совет",
                "gpt_answer": "Answer for the given question",
                "call_measurer": False,
                "photo_url": "http://example.com/photo.jpg"
            }
        }
from pydantic import BaseModel

class CityBase(BaseModel):
    name: str

class CityCreate(CityBase):
    pass

class City(CityBase):
    id: int

    class Config:
        from_attributes = True

class ManagerBase(BaseModel):
    username: str
    is_staff: bool
    is_admin: bool
    chat_id: str

class ManagerCreate(ManagerBase):
    hashed_password: str
    city_id: int

class Manager(ManagerBase):
    id: int
    identifier: str
    city: City

    class Config:
        from_attributes = True

class TokenData(BaseModel):
    user_id: int
    identifier: str
    username: str
    city: str | None = None
    is_staff: bool = False
    is_admin: bool = False
    chat_id: str | None = None
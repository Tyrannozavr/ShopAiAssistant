from sqlalchemy import Column, String, Boolean, Integer
from db import Base
import uuid

class Manager(Base):
    __tablename__ = "managers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    identifier = Column(String, unique=True, index=True, default=lambda: str(uuid.uuid4()))
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    city = Column(String, nullable=False)
    is_staff = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
    chat_id = Column(String, unique=True, nullable=True)  # Add this line

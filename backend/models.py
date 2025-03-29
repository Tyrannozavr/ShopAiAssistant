from sqlalchemy import Column, String, Boolean, Integer, Text, ForeignKey, func, DateTime
from sqlalchemy.orm import relationship
from fastapi import Request

from db import Base
import uuid

class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True, index=True, nullable=False)

    # Relationship to Manager
    managers = relationship("Manager", back_populates="city")

class Manager(Base):
    __tablename__ = "managers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    identifier = Column(String, unique=True, index=True, default=lambda: str(uuid.uuid4()))
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    city_id = Column(Integer, ForeignKey('cities.id'), nullable=True)
    is_staff = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
    chat_id = Column(String, unique=True, nullable=True)

    # Relationship to City
    city = relationship("City", back_populates="managers")


class ChatGPTInteraction(Base):
    __tablename__ = 'chatgpt_interactions'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, nullable=False)
    datetime = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    prompt = Column(String, nullable=False)
    response = Column(String, nullable=False)
    photo_url = Column(String, nullable=True)  # Store the URL of the photo

class Jokes(Base):
    __tablename__ = 'jokes'

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)

class Anecdote(Base):
    __tablename__ = 'anecdotes'

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String, nullable=False)
    door_type = Column(String, nullable=False)
    priorities = Column(String, nullable=False)  # Store as a comma-separated string
    contact = Column(String, nullable=False)
    username = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=True)
    address = Column(String, nullable=False)
    user_request = Column(String, nullable=True)
    gpt_answer = Column(String, nullable=True)
    call_measurer = Column(Boolean, default=False)
    file_id = Column(String, nullable=True)

    def __init__(self, city, door_type, priorities, contact, username, phone_number, first_name, last_name, address, user_request, gpt_answer, call_measurer, file_id):
        self.city = city
        self.door_type = door_type
        self.priorities = priorities
        self.contact = contact
        self.username = username
        self.phone_number = phone_number
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.user_request = user_request
        self.gpt_answer = gpt_answer
        self.call_measurer = call_measurer
        self.file_id = file_id

class Configuration(Base):
    __tablename__ = "configurations"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    key = Column(String, unique=True, index=True, nullable=False)
    value = Column(Text, nullable=False)
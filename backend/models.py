from sqlalchemy import Column, String, Boolean, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
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
    city_id = Column(Integer, ForeignKey('cities.id'), nullable=False)
    is_staff = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
    chat_id = Column(String, unique=True, nullable=True)

    # Relationship to City
    city = relationship("City", back_populates="managers")

class Configuration(Base):
    __tablename__ = "configurations"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    key = Column(String, unique=True, index=True, nullable=False)
    value = Column(Text, nullable=False)
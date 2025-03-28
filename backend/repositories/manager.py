from typing import Type

from sqlalchemy.orm import Session
from models import Manager
from errors.manager import ManagerNotFoundException

def get_manager_by_identifier(db: Session, identifier: str) -> Type[Manager]:
    manager = db.query(Manager).filter(Manager.identifier == identifier).first()
    if not manager:
        raise ManagerNotFoundException(identifier)
    return manager

def get_manager_by_username(db: Session, username: str) -> Type[Manager]:
    manager = db.query(Manager).filter(Manager.username == username).first()
    if not manager:
        raise ManagerNotFoundException(username)
    return manager
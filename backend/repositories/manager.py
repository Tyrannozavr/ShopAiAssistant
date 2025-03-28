from sqlalchemy.orm import Session
from typing_extensions import Type
from ..models import Manager
from ..errors.manager import ManagerNotFoundException

def get_manager_by_identifier(db: Session, identifier: str) -> Type[Manager]:
    manager = db.query(Manager).filter(Manager.identifier == identifier).first()
    if not manager:
        raise ManagerNotFoundException(identifier)
    return manager
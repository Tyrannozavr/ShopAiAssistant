import os

from depends.db import get_db
from models import Manager
from services.auth_service import get_hashed_password

from core.logging_config import logger


def seed_admin_user():
    db_session = next(get_db())
    admin_user = db_session.query(Manager).filter(Manager.is_admin == True).first()
    if not admin_user:
        admin_username = os.getenv("ADMIN_USERNAME")
        admin_password = os.getenv("ADMIN_PASSWORD")
        logger.info("Seeding admin user")
        if admin_username and admin_password:
            hashed_password = get_hashed_password(admin_password)
            new_admin = Manager(
                username=admin_username,
                hashed_password=hashed_password,
                is_staff=True,
                is_admin=True
            )
            db_session.add(new_admin)
            db_session.commit()
    db_session.close()

if __name__ == "__main__":
    seed_admin_user()
from starlette_admin.contrib.sqla import ModelView, Admin
from starlette_admin.fields import HasOne, HasMany

from db import engine
from models import City, Manager, Configuration
from services.auth_service import get_hashed_password

class CityAdmin(ModelView):
    identity = "city"
    label = "Cities"
    fields = [
        "id",
        "name",
        HasMany("managers", label="Managers"),
    ]

class ManagerAdmin(ModelView):
    identity = "manager"
    label = "Managers"
    fields = [
        "id",
        "identifier",
        "username",
        "hashed_password",
        HasOne("city", label="City"),
        "is_staff",
        "is_admin",
        "chat_id",
    ]

    async def create(self, data):
        # Hash the password before creating the user
        data["hashed_password"] = get_hashed_password(data.pop("password"))
        return await super().create(data)

    async def update(self, pk, data):
        # Hash the password if it's being updated
        if "password" in data:
            data["hashed_password"] = get_hashed_password(data.pop("password"))
        return await super().update(pk, data)

class ConfigurationAdmin(ModelView):
    identity = "configuration"
    label = "Configurations"
    fields = [
        "id",
        "key",
        "value",
    ]

admin = Admin(engine, title="Your Admin Title")

admin.add_view(CityAdmin(City))
admin.add_view(ManagerAdmin(Manager))
admin.add_view(ConfigurationAdmin(Configuration))

from typing import Optional

from starlette.requests import Request
from starlette_admin.contrib.sqla import ModelView
from starlette_admin.fields import HasOne, HasMany
from starlette_admin import BaseField
from dataclasses import dataclass
from starlette_admin.contrib.sqla import Admin as BaseAdmin


@dataclass
class CustomIdentifierField(BaseField):
    render_function_key: str = "customIdentifierRender"

from db import engine
from models import Configuration
from models import Manager, City


class CityAdmin(ModelView):
    identity = "city"
    label = "Cities"
    fields = [
        "id",
        "name",
        HasMany("managers", label="Managers", identity="manager"),
    ]


class ManagerAdmin(ModelView):
    identity = "manager"
    label = "Managers"
    model = Manager
    fields = [
        "id",
        "identifier",
        "username",
        "hashed_password",
        HasOne("city", label="City", identity="city"),
        "is_staff",
        "is_admin",
        "chat_id",
        CustomIdentifierField("custom_identifier", label="Custom Identifier"),
    ]



class ConfigurationAdmin(ModelView):
    identity = "configuration"
    label = "Configurations"
    fields = [
        "id",
        "key",
        "value",
    ]


class Admin(BaseAdmin):
    def custom_render_js(self, request: Request) -> Optional[str]:
        return request.url_for("static", path="js/custom_render.js")

admin = Admin(engine, title="Your Admin Title")

admin.add_view(CityAdmin(City))
admin.add_view(ManagerAdmin(Manager))
admin.add_view(ConfigurationAdmin(Configuration))
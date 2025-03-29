from typing import Optional
from starlette.requests import Request
from starlette_admin.contrib.sqla import ModelView
from starlette_admin.fields import HasOne, HasMany
from starlette_admin import BaseField
from dataclasses import dataclass
from starlette_admin.contrib.sqla import Admin as BaseAdmin
from db import engine
from models import Configuration, Manager, City, ChatGPTInteraction, Order, Jokes, Anecdote  # Import new models

@dataclass
class InviteField(BaseField):
    render_function_key: str = "inviteRender"

@dataclass
class CityInviteField(BaseField):
    render_function_key: str = "cityInviteRender"

class CityAdmin(ModelView):
    identity = "city"
    label = "Cities"
    fields = [
        "id",
        "name",
        HasMany("managers", label="Managers", identity="manager"),
        CityInviteField("city_invite", label="City Invite"),
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
        InviteField("invite", label="Invite"),
    ]

class ConfigurationAdmin(ModelView):
    identity = "configuration"
    label = "Configurations"
    fields = [
        "id",
        "key",
        "value",
    ]

class ChatGPTInteractionAdmin(ModelView):
    identity = "chatgpt_interaction"
    label = "ChatGPT Interactions"
    model = ChatGPTInteraction
    fields = [
        "id",
        "prompt",
        "response",
        "photo_url",
    ]

# New ModelView for Order
class OrderAdmin(ModelView):
    identity = "order"
    label = "Orders"
    model = Order
    fields = [
        "id",
        "city",
        "door_type",
        "priorities",
        "contact",
        "username",
        "phone_number",
        "first_name",
        "last_name",
        "address",
        "user_request",
        "gpt_answer",
        "call_measurer",
        "file_id",
    ]

# New ModelView for Jokes
class JokesAdmin(ModelView):
    identity = "jokes"
    label = "Jokes"
    model = Jokes
    fields = [
        "id",
        "text",
    ]

class AnecdoteAdmin(ModelView):
    identity = "anecdote"
    label = "Anecdotes"
    model = Anecdote
    fields = [
        "id",
        "text",
    ]

class Admin(BaseAdmin):
    def custom_render_js(self, request: Request) -> Optional[str]:
        return str(request.url_for("static", path="js/manager_render.js"))

admin = Admin(engine, title="Your Admin Title")

admin.add_view(CityAdmin(City))
admin.add_view(ManagerAdmin(Manager))
admin.add_view(ConfigurationAdmin(Configuration))
admin.add_view(ChatGPTInteractionAdmin(ChatGPTInteraction))
admin.add_view(OrderAdmin(Order))  # Register the Order admin view
admin.add_view(JokesAdmin(Jokes))  # Register the Jokes admin view
admin.add_view(AnecdoteAdmin(Anecdote))  # Register the Anecdote admin view

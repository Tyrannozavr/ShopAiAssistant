from importlib import import_module

from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse, RedirectResponse
from starlette_admin.contrib.sqla import Admin, ModelView
from fastapi import Request

from depends.db import get_db

models_module = import_module("app.models")


class AdminAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        """
        Dispatch method for the AdminAuthMiddleware.

        This method intercepts requests to the admin panel, verifies user authentication
        and authorization, and handles the request accordingly.

        Parameters:
        -----------
        request : Request
            The incoming HTTP request object.
        call_next : Callable
            The next middleware or route handler in the chain.

        Returns:
        --------
        Response
            The HTTP response, which could be a redirect, a JSON response, or the result
            of calling the next handler in the chain.

        Notes:
        ------
        - If the request path starts with "/admin", it checks for an access token in cookies.
        - If no token is found, it redirects to the login page.
        - If a token is found, it verifies if the user is a superadmin.
        - If the user is not a superadmin, it returns a 403 Forbidden response.
        - For non-admin routes or after successful authorization, it calls the next handler.
        """
        # Проверяем, начинается ли путь с /admin
        if request.url.path.startswith("/admin"):
            # Проверка токена или сессии
            token = request.cookies.get("access_token")
            if not token:
                return RedirectResponse("/superadmin/login", status_code=status.HTTP_303_SEE_OTHER)

            # Проверка прав пользователя
            try:
                db_session = next(get_db())
                user = get_user_by_token(token, db=db_session)  # Функция для получения пользователя
                db_session.close()
                if not user.is_superadmin:
                    return JSONResponse(status_code=403, content={"detail": "Forbidden"})
            except Exception as e:
                return JSONResponse(status_code=401, content={"detail": str(e)})

        # Продолжаем обработку запроса
        response = await call_next(request)
        return response


# Настройка Starlette Admin
admin = Admin(engine, title="Admin Panel")

# Define a mapping of model names to their custom admin views
admin_views = {
    "Product": ProductAdmin,
    "ProductAttribute": ProductAttributeAdmin,
    "ProductAttributeValue": ProductAttributeValueAdmin,
    "Shop": ShopAdmin,
    "ShopType": ShopTypeAdmin,
    "ShopTypeAttribute": ShopTypeAttributeAdmin,
}

# Регистрируем все модели из списка __all__
for model_name in models_module.__all__:
    model = getattr(models_module, model_name)
    view_class = admin_views.get(model_name, ModelView)

    # Use the model_name as the identity
    admin.add_view(view_class(model, identity=model_name.lower(), icon="fas fa-table"))

from flask import Flask
from .services.users.api import user_router


def register_blueprints(app: Flask):
    """
    Función que registra todos los blueprints con un prefijo común.
    """
    app.register_blueprint(user_router, url_prefix='/users')
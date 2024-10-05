from flask import Flask
from .router import register_blueprints
from config import Config
from .extensions import db
from flasgger import Swagger
from flask_jwt_extended import JWTManager

def create_app():

    #Inicializamos la app
    app = Flask(__name__)

    #Cargar la configuración
    app.config.from_object(Config)

    #Configuración de JWT
    JWTManager(app)

    #Configuración básica de Swagger
    Swagger(app)

    # Inicializar la base de datos
    db.init_app(app)

    #Configurar las rutas
    register_blueprints(app)


    return app
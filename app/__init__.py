from flask import Flask
from .router import register_blueprints
from config import Config
from .database import db
from flasgger import Swagger

def create_app():

    #Inicializamos la app
    app = Flask(__name__)

    #Configuración básica de Swagger
    swagger = Swagger(app)

    #Cargar la configuración
    app.config.from_object(Config)

    # Inicializar la base de datos
    db.init_app(app)

    #Configurar las rutas
    register_blueprints(app)


    return app
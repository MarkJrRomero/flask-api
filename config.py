from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'SECRETO-FLASK-APP-XLSP-2024'

    #Configuración de la base de datos PostgreSQL
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:123456@localhost:5432/flask-api'
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Desactivar para evitar advertencias

    # Evitar la creación de __pycache__
    PYTHONDONTWRITEBYTECODE = 1

    

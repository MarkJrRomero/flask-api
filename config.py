import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'xksdjfnoskdfnosfnskodfn'

    # Configuración de la base de datos SQLite
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Desactivar el sistema de seguimiento de modificaciones 

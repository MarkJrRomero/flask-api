from app.database import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Columna ID, clave primaria
    username = db.Column(db.String(64), unique=True, nullable=False)  # Nombre de usuario único y no nulo
    email = db.Column(db.String(120), unique=True, nullable=False)  # Email único y no nulo
    password_hash = db.Column(db.String(128))  # Hash de la contraseña
    
    def set_password(self, password):
        """Genera un hash para almacenar la contraseña de forma segura"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verifica que el hash de la contraseña coincide con el proporcionado"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'password_hash': self.password_hash
        }

    def __repr__(self):
        return f'<User {self.username}>'
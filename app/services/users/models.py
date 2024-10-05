from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

# Tabla intermedia entre Usuario y Rol
user_roles = db.Table('user_roles',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Columna ID, clave primaria
    username = db.Column(db.String(64), unique=True, nullable=False)  # Nombre de usuario único y no nulo
    email = db.Column(db.String(120), unique=True, nullable=False)  # Email único y no nulo
    password_hash = db.Column(db.String(128))  # Hash de la contraseña
    roles = db.relationship('Role', secondary=user_roles, backref=db.backref('users', lazy='dynamic'))
    
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
    


# Tabla intermedia entre Rol y Permiso
role_permissions = db.Table('role_permissions',
    db.Column('role_id', db.Integer, db.ForeignKey('role.id')),
    db.Column('permission_id', db.Integer, db.ForeignKey('permission.id'))
)

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    permissions = db.relationship('Permission', secondary=role_permissions, backref=db.backref('roles', lazy='dynamic'))

    def __repr__(self):
        return f'<Role {self.name}>'
    
    
class Permission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    
    def __repr__(self):
        return f'<Permission {self.name}>'
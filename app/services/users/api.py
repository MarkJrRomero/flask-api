from flask import Blueprint, jsonify, request, json
from .models import User
from app.database import db
from flasgger import swag_from

# Crear un blueprint para el servicio de usuario
user_router = Blueprint('user_bp', __name__)


@user_router.route('/list/', methods=['GET'])
@swag_from({
    'responses': {
        200: {
            'description': 'Usuarios consultados correctamente',
            'examples': {
                'application/json': {
                    'data': [
                        {'id': 1, 'username': 'usuario1', 'email': 'usuario1@example.com'},
                        {'id': 2, 'username': 'usuario2', 'email': 'usuario2@example.com'}
                    ]
                }
            }
        }
    },
    'tags': ['Users']
})
def get_users():
    users = User.query.all()

    # Convertir la lista de objetos User en un formato JSON serializable
    users_list = [user.to_dict() for user in users]
    return jsonify({"data": users_list, "message": "Usuarios consultados correctamente", "status": 200}), 200

@user_router.route('/create', methods=['POST'])
@swag_from({
    'responses': {
        201: {
            'description': 'Usuario creado exitosamente',
            'examples': {
                'application/json': {
                    'message': 'Usuario creado exitosamente'
                }
            }
        },
        400: {
            'description': 'Error en la solicitud',
            'examples': {
                'application/json': {
                    'error': 'El usuario o email ya están registrados'
                }
            }
        }
    },
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'username': {'type': 'string'},
                    'email': {'type': 'string'},
                    'password': {'type': 'string'}
                },
                'required': ['username', 'email', 'password']
            }
        }
    ],
    'tags': ['Users']
})
def create_users():
    data_post = request.get_json()

    # Validar que los campos requeridos están presentes
    if not data_post or not all(key in data_post for key in ('username', 'email', 'password')):
        return jsonify({"error": "Faltan campos obligatorios (username, email, password)"}), 404
    
    username = data_post['username']
    email = data_post['email']
    password = data_post['password']

    # Verificar si el usuario o email ya existen en la base de datos
    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
        return jsonify({"error": "El usuario o email ya están registrados"}), 400

    # Crear una nueva instancia de usuario
    new_user = User(username=username, email=email)
    new_user.set_password(password)  # Almacenar la contraseña hasheada
    
    # Guardar el nuevo usuario en la base de datos
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": f"Usuario {username} creado exitosamente"}), 201


@user_router.route('/login', methods=['POST'])
@swag_from({
    'responses': {
        200: {
            'description': 'Inicio de sesión exitoso',
            'examples': {
                'application/json': {
                    'message': 'Inicio de sesión exitoso'
                }
            }
        },
        401: {
            'description': 'Credenciales inválidas',
            'examples': {
                'application/json': {
                    'error': 'Credenciales inválidas'
                }
            }
        }
    },
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'username': {'type': 'string'},
                    'password': {'type': 'string'}
                },
                'required': ['username', 'password']
            }
        }
    ],
    'tags': ['Users']
})
def login_users():
    data_post = request.get_json()
    
    username = data_post['username']
    password = data_post['password']

    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        return jsonify({"message": "Inicio de sesión exitoso"}), 200
    else:
        return jsonify({"error": "Credenciales inválidas"}), 401

from flask import Blueprint, request, jsonify
from app.models import User
from app import db
from flask_jwt_extended import create_access_token
import logging # Para registrar erros

# Cria o Blueprint de autenticação
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Endpoint para registrar um novo usuário.
    Espera um JSON com "username" e "password".
    """
    try:
        # Pega os dados do corpo da requisição (JSON)
        data = request.get_json()
        
        username = data.get('username')
        password = data.get('password')

        # Validação simples
        if not username or not password:
            return jsonify({"error": "Username e password são obrigatórios"}), 400

        # Verifica se o usuário já existe
        if User.query.filter_by(username=username).first():
            return jsonify({"error": "Username já existe"}), 409 # 409 = Conflict

        # Cria o novo usuário (o __init__ do modelo User vai hashear a senha)
        new_user = User(username=username, password=password)
        
        # Adiciona ao banco de dados
        db.session.add(new_user)
        db.session.commit()

        # Retorna uma resposta de sucesso
        return jsonify({
            "message": "Usuário registrado com sucesso!",
            "user": {"id": new_user.id, "username": new_user.username}
        }), 201 # 201 = Created

    except Exception as e:
        # Em caso de erro, desfaz qualquer mudança no banco
        db.session.rollback()
        logging.error(f"Erro ao registrar: {e}")
        return jsonify({"error": "Erro interno ao registrar usuário"}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Endpoint de login.
    Espera "username" e "password", retorna um access_token JWT.
    """
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({"error": "Username e password são obrigatórios"}), 400

        # Procura o usuário no banco
        user = User.query.filter_by(username=username).first()

        # Verifica se o usuário existe E se a senha está correta
        if user and user.check_password(password):
            # Gera o token de acesso (JWT)
            # A 'identity' é o que será armazenado dentro do token (neste caso, o ID do usuário)
            access_token = create_access_token(identity=user.id)
            
            return jsonify({
                "message": "Login bem-sucedido!",
                "access_token": access_token
            }), 200 # 200 = OK

        # Se o usuário não existir ou a senha estiver errada
        return jsonify({"error": "Credenciais inválidas"}), 401 # 401 = Unauthorized

    except Exception as e:
        logging.error(f"Erro no login: {e}")
        return jsonify({"error": "Erro interno ao fazer login"}), 500
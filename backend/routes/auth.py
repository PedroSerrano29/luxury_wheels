from flask import Blueprint, jsonify, request, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Cliente
import jwt
import datetime

clientes_bp = Blueprint ('Cliente', __name__)

### POST /api/auth/registo ###
@clientes_bp.route('/api/auth/registo', methods=['POST'])
def registar_cliente():
    dados = request.get_json()

    nome = dados.get('nome')
    email = dados.get('email')
    password = dados.get('password')
    password_confirm = dados.get('password_confirm')

    # Validar se as passwords coincidem
    if password != password_confirm:
        return jsonify({"erro": "As passwords não coincidem"}), 400

    # Validar que o email ainda não existe
    ja_existe = Cliente.query.filter_by(email=email).first() is not None
    if ja_existe:
        return jsonify({"erro": "Utilizador já existe"}), 400

    # Criar o novo cliente
    novo_cliente = Cliente(
        nome = nome,
        email = email,
        password_hash = generate_password_hash(password)
    )

    db.session.add(novo_cliente)
    db.session.commit()

    return jsonify({"id": novo_cliente.id, "mensagem": "Utilizador registado com sucesso"}), 201


### POST /api/auth/login ###

@clientes_bp.route('/api/auth/login', methods=['POST'])
def login_cliente():
    dados =request.get_json()

    email = dados.get('email')
    password = dados.get('password')

    cliente = Cliente.query.filter_by(email=email).first()
    if cliente is None or not check_password_hash(cliente.password_hash, password):
        return jsonify({"erro": "Credenciais inválidas"}), 401

    token =jwt.encode(
        {
            "cliente_id": cliente.id,
            "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=24)
            },
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
    )

    return jsonify({
        "id": cliente.id,
        "nome": cliente.nome,
        "email": cliente.email,
        "token": token,
        "mensagem": "Login efetuado com sucesso"
    })
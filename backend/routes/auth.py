from flask import Blueprint, jsonify, request, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Cliente, Utilizador
import jwt
import datetime

clientes_bp = Blueprint ('Cliente', __name__)

### POST /api/auth/registo ###
@clientes_bp.route('/api/auth/registo', methods=['POST'])
def registar_cliente():
    corpo = request.get_json()

    nome = corpo.get('nome')
    email = corpo.get('email')
    password = corpo.get('password')
    password_confirm = corpo.get('password_confirm')

    # Validar campos obrigatórios (a API pode ser chamada sem o formulário)
    if not nome or not nome.strip() or not email or not email.strip() or not password:
        return jsonify({"erro": "Nome, email e password são obrigatórios"}), 400

    if '@' not in email:
        return jsonify({"erro": "Email inválido"}), 400

    if len(password) < 6:
        return jsonify({"erro": "A password deve ter pelo menos 6 caracteres"}), 400

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
    corpo = request.get_json()

    email = corpo.get('email')
    password = corpo.get('password')

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

### POST /api/auth/login-staff ### - Login de utilizador

@clientes_bp.route('/api/auth/login-staff', methods=['POST'])
def login_staff():
    corpo = request.get_json()
    email = corpo.get('email')
    password = corpo.get('password')

    utilizador = Utilizador.query.filter_by(email=email).first()

    if utilizador is None or not check_password_hash(utilizador.password_hash, password):
        return jsonify({"erro": "Credenciais inválidas"}), 401

    token = jwt.encode(
        {
            "utilizador_id": utilizador.id,
            "role": utilizador.role,
            "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=24)
        },
        current_app.config['SECRET_KEY'],
        algorithm="HS256"
    )

    return jsonify({
        "id": utilizador.id,
        "nome": utilizador.nome,
        "email": utilizador.email,
        "role": utilizador.role,
        "token": token,
        "mensagem": "Login efetuado com sucesso"
    })
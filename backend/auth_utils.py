from functools import wraps
from flask import request, jsonify, current_app
import jwt

def token_obrigatorio(funcao_original):
    @wraps(funcao_original)
    def funcao_envolvida(*args, **kwargs):
        token =request.headers.get('Authorization')

        if not token:
            return jsonify({"erro": "Token em falta"}), 401

        try:
            dados = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({"erro": "Token expirado"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"erro": "Token inválido"}), 401

        return funcao_original(*args, **kwargs)
    return funcao_envolvida
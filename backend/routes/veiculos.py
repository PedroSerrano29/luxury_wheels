from flask import Blueprint

veiculos_bp = Blueprint('veiculos', __name__)

@veiculos_bp.route('api/veiculos', methods=['GET'])
def listar_veiculos():
    return {"mensagem": "ainda vazio"}
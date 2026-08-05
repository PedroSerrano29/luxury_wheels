from flask import Blueprint, jsonify
from models import Veiculo

veiculos_bp = Blueprint('veiculos', __name__)

@veiculos_bp.route('/api/veiculos', methods=['GET'])
def listar_veiculos():
    veiculos = Veiculo.query.all()
    resultado = [
        {
            "id": v.id,
            "marca": v.marca,
            "modelo": v.modelo,
            "categoria": v.categoria,
            "transmissao": v.transmissao,
            "tipo": v.tipo,
            "capacidade_pessoas": v.capacidade_pessoas,
            "valor_diaria": v.valor_diaria,
            "imagem_url": v.imagem_url,
            "disponivel": v.disponivel
        }
        for v in veiculos
    ]
    return jsonify(resultado)

#funcao teste
@veiculos_bp.route('/api/veiculos/<int:veiculo_id>', methods=['GET'])
def obter_veiculo(veiculo_id):
    v = Veiculo.query.get(veiculo_id)

    if v is None:
        return jsonify({"erro": "Veículo não encontrado"}), 404

    return jsonify({
        "id": v.id,
        "marca": v.marca,
        "modelo": v.modelo,
        "categoria": v.categoria,
        "transmissao": v.transmissao,
        "tipo": v.tipo,
        "capacidade_pessoas": v.capacidade_pessoas,
        "valor_diaria": v.valor_diaria,
        "imagem_url": v.imagem_url,
        "disponivel": v.disponivel,
    })
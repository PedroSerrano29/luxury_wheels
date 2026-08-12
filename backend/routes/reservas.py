from flask import Blueprint, jsonify, request, current_app
from models import db, Reserva, Veiculo
from auth_utils import token_obrigatorio
from datetime import datetime as dt

reserva_bd = Blueprint('Reserva', __name__)

def veiculo_disponivel_no_periodo(veiculo_id, data_inicio, data_fim):
    conflito = Reserva.query.filter(
        Reserva.veiculo_id == veiculo_id,
        Reserva.estado == 'Ativa',
        Reserva.data_inicio <= data_fim,
        Reserva.data_fim >= data_inicio
    ).first()

    return conflito is None

### POST /api/reservas ### - Fazer reserva

@reserva_bd.route('/api/reservas', methods=['POST'])
@token_obrigatorio
def criar_reserva(dados):
    cliente_id = dados.get('cliente_id') # vem do TOKEN, nunca do JSON enviado
    corpo = request.get_json()

    veiculo_id = corpo.get('veiculo_id')
    data_inicio = corpo.get('data_inicio')
    data_fim = corpo.get('data_fim')
    forma_pagamento_id = corpo.get('forma_pagamento_id')

    veiculo = Veiculo.query.get(veiculo_id)
    if veiculo is None:
        return jsonify({"erro": "Veículo não encontrado"}), 404

    if not veiculo.ativo or veiculo.em_manutencao:
        return jsonify({"erro": "Veículo não está disponivel para aluguer"}), 409

    if not veiculo_disponivel_no_periodo(veiculo_id, data_inicio, data_fim):
        return jsonify({"erro": "Veículo ja tem um reserva para essas datas"}), 409

    data_inicio_obj = dt.strptime(data_inicio, "%Y-%m-%d").date()
    data_fim_obj = dt.strptime(data_fim, "%Y-%m-%d").date()

    if data_fim_obj <= data_inicio_obj:
        return jsonify({"erro": "A data de fim deve ser posterior à data de inicio"}), 400

    numero_dias = (data_fim_obj - data_inicio_obj).days
    valor_total = veiculo.valor_diaria * numero_dias

    nova_reserva = Reserva(
        cliente_id=cliente_id,
        veiculo_id=veiculo_id,
        data_inicio=data_inicio,
        data_fim=data_fim,
        valor_total=valor_total,
        forma_pagamento_id=forma_pagamento_id,
        estado='Ativa'
    )

    veiculo.disponivel = False

    db.session.add(nova_reserva)
    db.session.commit()

    return jsonify({
        "id": nova_reserva.id,
        "valor_total": valor_total,
        "mensagem": "Reserva criada com sucesso"
    }), 201
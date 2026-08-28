from flask import Blueprint, jsonify, request, current_app
from models import db, Reserva, Veiculo
from auth_utils import token_obrigatorio
from services.reservas_service import (
    ErroReserva,
    validar_datas_reserva,
    veiculo_disponivel_no_periodo
)
from services.pagamentos_service import obter_ou_criar_forma_pagamento

reserva_bd = Blueprint('Reserva', __name__)

### POST /api/reservas ### - Fazer reserva

@reserva_bd.route('/api/reservas', methods=['POST'])
@token_obrigatorio
def criar_reserva(dados):
    cliente_id = dados.get('cliente_id') # vem do TOKEN, nunca do JSON enviado
    corpo = request.get_json()

    veiculo_id = corpo.get('veiculo_id')
    data_inicio = corpo.get('data_inicio')
    data_fim = corpo.get('data_fim')
    forma_pagamento_tipo = corpo.get('forma_pagamento_tipo')

    veiculo = Veiculo.query.get(veiculo_id)
    if veiculo is None:
        return jsonify({"erro": "Veículo não encontrado"}), 404

    if not veiculo.ativo or veiculo.em_manutencao:
        return jsonify({
            "erro": "Veículo não está disponivel para aluguer"
            }), 409

    try:
        data_inicio_obj, data_fim_obj = validar_datas_reserva(
            data_inicio,
            data_fim
        )
    except ErroReserva as erro:
        return jsonify({"erro": erro.mensagem}), erro.status_code

    if not veiculo_disponivel_no_periodo(
        veiculo_id,
        data_inicio_obj,
        data_fim_obj
    ):
        return jsonify({
            "erro" :"Veículo ja tem uma reserva para essas datas"
        }), 409

    forma = obter_ou_criar_forma_pagamento(cliente_id, forma_pagamento_tipo)

    numero_dias = (data_fim_obj - data_inicio_obj).days
    valor_total = veiculo.valor_diaria * numero_dias

    nova_reserva = Reserva(
        cliente_id=cliente_id,
        veiculo_id=veiculo_id,
        data_inicio=data_inicio,
        data_fim=data_fim,
        valor_total=valor_total,
        forma_pagamento_id=forma.id,
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

@reserva_bd.route('/api/reservas', methods=['GET'])
@token_obrigatorio
def listar_reserva(dados):
    cliente_id = dados.get('cliente_id')

    reservas = Reserva.query.filter_by(cliente_id=cliente_id).all()
    resultado = [r.to_dict() for r in reservas]

    return jsonify(resultado)

    ### PUT /api/reservas/<id> ###

@reserva_bd.route('/api/reservas/<int:reserva_id>', methods=['PUT'])
@token_obrigatorio
def alterar_reserva(dados, reserva_id):
    cliente_id_token = dados.get('cliente_id')

    reserva = Reserva.query.get(reserva_id)
    if reserva is None:
        return jsonify({"erro": "Reserva não encontrada"}), 404

    if reserva.cliente_id != cliente_id_token:
        return jsonify({"erro": "Não tens permissão para alterar esta reserva"}), 403

    corpo = request.get_json()
    if corpo.get('cancelar'):
        reserva.estado = 'Cancelada'

        veiculo = Veiculo.query.get(reserva.veiculo_id)
        veiculo.disponivel = True

        db.session.commit()
        return jsonify({"mensagem": "Reserva cancelada com sucesso"})

    nova_data_inicio = corpo.get('data_inicio', reserva.data_inicio)
    nova_data_fim = corpo.get('data_fim', reserva.data_fim)

    try:
        data_inicio_obj, data_fim_obj = validar_datas_reserva(
            nova_data_inicio,
            nova_data_fim
        )
    except ErroReserva as erro:
        return jsonify({"erro": erro.mensagem}), erro.status_code

    if not veiculo_disponivel_no_periodo(
        reserva.veiculo_id,
        data_inicio_obj,
        data_fim_obj,
        reserva_id
    ):
        return jsonify({
            "erro": "Já existe outra reserva para essas datas"
        }), 409

    veiculo = Veiculo.query.get(reserva.veiculo_id)
    numero_dias = (data_fim_obj - data_inicio_obj).days

    reserva.data_inicio = nova_data_inicio
    reserva.data_fim = nova_data_fim
    reserva.valor_total = veiculo.valor_diaria * numero_dias

    db.session.commit()

    return jsonify({"mensagem": "Reserva atualizada com sucesso", "novo_valor_total": reserva.valor_total})
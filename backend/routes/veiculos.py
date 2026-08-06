from flask import Blueprint, jsonify, request
from models import Veiculo

def mapear_capacidade(grupo):
    mapa = {
        "1-4": (1, 4),
        "5-6": (5, 6),
        "mais_de_7": (7, None),
    }
    return mapa.get(grupo, (None, None))

veiculos_bp = Blueprint('veiculos', __name__)

@veiculos_bp.route('/api/veiculos', methods=['GET'])
def listar_veiculos():
    query = Veiculo.query

    categoria = request.args.get('categoria')
    if categoria:
        query = query.filter_by(categoria=categoria)

    if tipo := request.args.get('tipo'): # a mesma funçao que a de cima, mas usando o walrus operator
        query = query.filter_by(tipo=tipo)

    if transmissao := request.args.get('transmissao'):
        query = query.filter_by(transmissao=transmissao)

    if valor_maximo := request.args.get('valor_maximo'):
        query = query.filter(Veiculo.valor_diaria <= float(valor_maximo))    

    grupo_capacidade = request.args.get('capacidade_pessoas')
    if grupo_capacidade:
        minimo, maximo = mapear_capacidade(grupo_capacidade)
        if minimo is not None:
            query = query.filter(Veiculo.capacidade_pessoas >= minimo)
        if maximo is not None:
            query = query.filter(Veiculo.capacidade_pessoas <= maximo)

    veiculos = query.all()
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
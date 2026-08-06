from flask import Blueprint, jsonify, request
from models import db, Veiculo

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
    resultado = [v.to_dict() for v in veiculos]
    return jsonify(resultado)

#funcao teste
@veiculos_bp.route('/api/veiculos/<int:veiculo_id>', methods=['GET'])
def obter_veiculo(veiculo_id):
    v = Veiculo.query.get(veiculo_id)

    if v is None:
        return jsonify({"erro": "Veículo não encontrado"}), 404

    return jsonify(v.to_dict())

### Funções para a gestão de frotas de veículos ###

### POST /api/veiculos (criar) ###

@veiculos_bp.route('/api/veiculos', methods=['POST'])
def criar_veiculo():
    dados = request.get_json()

    novo_veiculo = Veiculo(
        marca=dados['marca'],
        modelo=dados['modelo'],
        matricula=dados.get('matricula'),
        combustivel=dados.get('combustivel'),
        categoria=dados['categoria'],
        transmissao=dados['transmissao'],
        tipo=dados['tipo'],
        capacidade_pessoas=dados['capacidade_pessoas'],
        valor_diaria=dados['valor_diaria'],
        imagem_url=dados.get('imagem_url'),
        data_ultima_revisao=dados.get('data_ultima_revisao'),
        data_proxima_revisao=dados.get('data_proxima_revisao'),
        data_ultima_inspecao=dados.get('data_ultima_inspecao'),
    )

    db.session.add(novo_veiculo)
    db.session.commit()

    return jsonify({"id": novo_veiculo.id, "mensagem": "Veículo criado com sucesso"}), 201

### PUT /api/veiculos/<id> (alterar) ###

@veiculos_bp.route('/api/veiculos/<int:veiculo_id>', methods=['PUT'])
def atualizar_veiculo(veiculo_id):
    v = Veiculo.query.get(veiculo_id)

    if v is None:
        return jsonify({"erro": "Veículo não encontrado"}), 404

    dados = request.get_json()

    if 'marca' in dados:
        v.marca = dados['marca']
    if 'modelo' in dados:
        v.modelo = dados['modelo']
    if 'valor_diaria' in dados:
        v.valor_diaria = dados['valor_diaria']
    if 'matricula' in dados:
        v.matricula = dados['matricula']
    if 'combustivel' in dados:
        v.combustivel = dados['combustivel']
    if 'categoria' in dados:
        v.categoria = dados['categoria']
    if 'transmissao' in dados:
        v.transmissao = dados['transmissao']
    if 'tipo' in dados:
        v.tipo = dados['tipo']
    if 'capacidade_pessoas' in dados:
        v.capacidade_pessoas = dados['capacidade_pessoas']
    if 'imagem_url' in dados:
        v.imagem_url = dados['imagem_url']
    if 'data_ultima_revisao' in dados:
        v.data_ultima_revisao = dados['data_ultima_revisao']
    if 'data_proxima_revisao' in dados:
        v.data_proxima_revisao = dados['data_proxima_revisao']
    if 'data_ultima_inspecao' in dados:
        v.data_ultima_inspecao = dados['data_ultima_inspecao']
    if 'disponivel' in dados:
        v.disponivel = dados['disponivel']
    if 'em_manutencao' in dados:
        v.em_manutencao = dados['em_manutencao']

    db.session.commit()

    return jsonify({"mensagem": "Veículo atualizado com sucesso"})
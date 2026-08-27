from flask import Blueprint, jsonify, request
from models import db, Veiculo, Reserva
from auth_utils import token_obrigatorio  

GRUPO_CAPACIDADE = {
        "1-4": (1, 4),
        "5-6": (5, 6),
        "mais_de_7": (7, None),
    }

def mapear_capacidade(grupo):
    return GRUPO_CAPACIDADE.get(grupo, (None, None))

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

@veiculos_bp.route('/api/veiculos/opcoes-filtro', methods=['GET'])
def opcoes_filtro():
    tipos = db.session.query(Veiculo.tipo).distinct().all()
    tipos = [t[0] for t in tipos]

    categorias_por_tipo = {}
    for tipo in tipos:
        categorias = db.session.query(Veiculo.categoria).filter_by(tipo=tipo).distinct().all()
        categorias_por_tipo[tipo] = [c[0] for c in categorias]

    transmissoes = db.session.query(Veiculo.transmissao).distinct().all()
    transmissoes = [t[0] for t in transmissoes]

    return jsonify({
        "tipos": tipos,
        "categorias_por_tipo": categorias_por_tipo,
        "transmissoes": transmissoes,
        "grupos_capacidade": list(GRUPO_CAPACIDADE.keys())
    })


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
@token_obrigatorio
def criar_veiculo(dados):
    if dados.get('role') not in ('gestor','admin'):
        return jsonify({"erro": "Ação não autorizada"}), 403

    corpo = request.get_json()

    novo_veiculo = Veiculo(
        marca=corpo['marca'],   # <- dados['marca'] passa a corpo['marca']
        modelo=corpo['modelo'],
        matricula=corpo.get('matricula'),
        combustivel=corpo.get('combustivel'),
        categoria=corpo['categoria'],
        transmissao=corpo['transmissao'],
        tipo=corpo['tipo'],
        capacidade_pessoas=corpo['capacidade_pessoas'],
        valor_diaria=corpo['valor_diaria'],
        imagem_url=corpo.get('imagem_url'),
        data_ultima_revisao=corpo.get('data_ultima_revisao'),
        data_proxima_revisao=corpo.get('data_proxima_revisao'),
        data_ultima_inspecao=corpo.get('data_ultima_inspecao'),
    )

    db.session.add(novo_veiculo)
    db.session.commit()

    return jsonify({"id": novo_veiculo.id, "mensagem": "Veículo criado com sucesso"}), 201

### PUT /api/veiculos/<id> (alterar) ###

@veiculos_bp.route('/api/veiculos/<int:veiculo_id>', methods=['PUT'])
@token_obrigatorio
def atualizar_veiculo(dados, veiculo_id):
    if dados.get('role') not in ('gestor','admin'):
        return jsonify({"erro": "Ação não autorizada"}), 403

    v = Veiculo.query.get(veiculo_id)

    if v is None:
        return jsonify({"erro": "Veículo não encontrado"}), 404



    corpo = request.get_json()

    if 'marca' in corpo:
        v.marca = corpo['marca']
    if 'modelo' in corpo:
        v.modelo = corpo['modelo']
    if 'valor_diaria' in corpo:
        v.valor_diaria = corpo['valor_diaria']
    if 'matricula' in corpo:
        v.matricula = corpo['matricula']
    if 'combustivel' in corpo:
        v.combustivel = corpo['combustivel']
    if 'categoria' in corpo:
        v.categoria = corpo['categoria']
    if 'transmissao' in corpo:
        v.transmissao = corpo['transmissao']
    if 'tipo' in corpo:
        v.tipo = corpo['tipo']
    if 'capacidade_pessoas' in corpo:
        v.capacidade_pessoas = corpo['capacidade_pessoas']
    if 'imagem_url' in corpo:
        v.imagem_url = corpo['imagem_url']
    if 'data_ultima_revisao' in corpo:
        v.data_ultima_revisao = corpo['data_ultima_revisao']
    if 'data_proxima_revisao' in corpo:
        v.data_proxima_revisao = corpo['data_proxima_revisao']
    if 'data_ultima_inspecao' in corpo:
        v.data_ultima_inspecao = corpo['data_ultima_inspecao']
    if 'disponivel' in corpo:
        v.disponivel = corpo['disponivel']
    if 'em_manutencao' in corpo:
        v.em_manutencao = corpo['em_manutencao']

    db.session.commit()

    return jsonify({"mensagem": "Veículo atualizado com sucesso"})

### Soft delete — PUT /api/veiculos/<id>/desativar ###
@veiculos_bp.route('/api/veiculos/<int:veiculo_id>/desativar', methods=['PUT'])
@token_obrigatorio
def desativar_veiculo(dados, veiculo_id):
    if dados.get('role') not in ('gestor','admin'):
        return jsonify({"erro": "Ação não autorizada"}), 403
    
    v = Veiculo.query.get(veiculo_id)
    if v is None:
        return jsonify({"erro": "Veículo não encontrado"}), 404

    v.ativo = False
    v.disponivel = False
    db.session.commit()

    return jsonify({"mensagem": "Veículo desativado com sucesso"})

### Hard delete — DELETE /api/veiculos/<id> ###
# precisa de importar Reserva também

@veiculos_bp.route('/api/veiculos/<int:veiculo_id>', methods=['DELETE'])
@token_obrigatorio
def apagar_veiculo(dados, veiculo_id):
    if dados.get('role') != 'admin':
        return jsonify({"erro": "Apenas administradores podem apagar veículos"}), 403
    
    v = Veiculo.query.get(veiculo_id)
    if v is None:
        return jsonify({"erro": "Veículo não encontrado"}), 404

    tem_reservas = Reserva.query.filter_by(veiculo_id=veiculo_id).first() is not None
    if tem_reservas:
        return jsonify({"erro": "Não é possível apagar: veículo tem reservas associadas. Use desativar em vez disso."}), 409

    db.session.delete(v)
    db.session.commit()

    return jsonify({"mensagem": "Veículo apagado permanentemente"})
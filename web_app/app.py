from flask import request, render_template
from datetime import datetime, timedelta
from setup_database import Veiculo, Reserva, Session
from sqlalchemy import or_, and_

def home():
    query = session.query(Veiculo)

    # Filtros via GET
    categoria = request.args.get('categoria')
    transmissao = request.args.get('transmissao')
    tipo = request.args.get('tipo')
    lugares = request.args.get('lugares')
    data_inicio = request.args.get('data_inicio')
    data_fim = request.args.get('data_fim')

    if categoria:
        query = query.filter_by(categoria=categoria)
    if transmissao:
        query = query.filter_by(transmissao=transmissao)
    if tipo:
        query = query.filter_by(tipo=tipo)
    if lugares:
        if lugares == '1-4':
            query = query.filter(Veiculo.lugares.between(1, 4))
        elif lugares == '5-6':
            query = query.filter(Veiculo.lugares.between(5, 6))
        elif lugares == '7+':
            query = query.filter(Veiculo.lugares >= 7)

    hoje = datetime.today().date()
    um_ano_atras = hoje - timedelta(days=365)

    veiculos = query.all()
    veiculos_info = []

    for veiculo in veiculos:
        indisponivel = False
        motivos = []

        # Verificações de disponibilidade
        if not veiculo.disponivel:
            indisponivel = True
            motivos.append('Disponibilidade desativada')

        if veiculo.ultima_inspecao and veiculo.ultima_inspecao < um_ano_atras:
            indisponivel = True
            motivos.append('Inspeção fora de validade')

        if veiculo.proxima_revisao and veiculo.proxima_revisao <= hoje:
            indisponivel = True
            motivos.append('Revisão expirada')

        # Verifica conflitos com reservas
        if data_inicio and data_fim:
            try:
                inicio = datetime.strptime(data_inicio, "%Y-%m-%d").date()
                fim = datetime.strptime(data_fim, "%Y-%m-%d").date()

                reservas_existentes = session.query(Reserva).filter(
                    Reserva.veiculo_id == veiculo.id,
                    Reserva.data_inicio <= fim,
                    Reserva.data_fim >= inicio
                ).all()

                if reservas_existentes:
                    indisponivel = True
                    motivos.append('Reservado no período selecionado')
            except ValueError:
                pass  # Ignora datas mal formatadas

        veiculos_info.append({
            'id': veiculo.id,
            'marca': veiculo.marca,
            'modelo': veiculo.modelo,
            'categoria': veiculo.categoria,
            'transmissao': veiculo.transmissao,
            'tipo': veiculo.tipo,
            'lugares': veiculo.lugares,
            'valor_diaria': veiculo.diaria,
            'imagem': veiculo.imagem if veiculo.imagem else 'default.jpg',
            'indisponivel': indisponivel,
            'motivos': motivos
        })

    return render_template('home.html', veiculos=veiculos_info)

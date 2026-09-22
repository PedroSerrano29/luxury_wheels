import argparse
from datetime import date
from app import create_app
from models import db, Veiculo
from services.veiculos_service import (
    motivo_indisponibilidade,
    registar_inspecao,
    registar_revisao,
    texto_para_data
)

# Ferramenta de linha de comandos para o gestor da frota.
# Exemplos:
#   python registar_manutencao.py                     -> lista os veículos indisponíveis e o motivo
#   python registar_manutencao.py 18 inspecao         -> inspeção feita hoje no veículo 18
#   python registar_manutencao.py 22 revisao 2026-09-20

def listar_indisponiveis(hoje):
    indisponiveis = 0
    for veiculo in Veiculo.query.order_by(Veiculo.id).all():
        motivo = motivo_indisponibilidade(veiculo, hoje)
        if motivo:
            indisponiveis += 1
            print(f"{veiculo.id:>3}  {veiculo.marca} {veiculo.modelo:<20} {motivo}")
    print(f"{indisponiveis} veículo(s) indisponível(eis) em {hoje.isoformat()}.")

def main():
    parser = argparse.ArgumentParser(description='Regista inspeções e revisões dos veículos.')
    parser.add_argument('veiculo_id', nargs='?', type=int)
    parser.add_argument('tipo', nargs='?', choices=['inspecao', 'revisao'])
    parser.add_argument('data', nargs='?', help='AAAA-MM-DD (por defeito, hoje)')
    args = parser.parse_args()

    hoje = date.today()

    with create_app().app_context():
        if args.veiculo_id is None:
            listar_indisponiveis(hoje)
            return

        if args.tipo is None:
            parser.error('indique o tipo: inspecao ou revisao')

        veiculo = db.session.get(Veiculo, args.veiculo_id)
        if veiculo is None:
            parser.error(f'veículo {args.veiculo_id} não encontrado')

        try:
            data = texto_para_data(args.data) if args.data else hoje
        except ValueError:
            parser.error('a data deve estar no formato AAAA-MM-DD')

        if data > hoje:
            parser.error('não se pode registar uma manutenção no futuro')

        if args.tipo == 'inspecao':
            registar_inspecao(veiculo, data)
        else:
            registar_revisao(veiculo, data)
        db.session.commit()

        print(f"{veiculo.marca} {veiculo.modelo}: {args.tipo} registada a {data.isoformat()}.")
        print(f"Estado: {motivo_indisponibilidade(veiculo, hoje) or 'disponível para aluguer'}")

if __name__ == '__main__':
    main()

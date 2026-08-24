from datetime import datetime as dt
from models import Reserva, Veiculo

class ErroReserva(Exception):
    def __init__(self, mensagem, status_code=400):
        self.mensagem = mensagem
        self.status_code = status_code
        super().__init__(mensagem)

def validar_datas_reserva(data_inicio, data_fim):
    if not data_inicio or not data_fim:
        raise ErroReserva(
            'As datas de início e fim são obrigatórias.'
        )

    try:
        inicio = dt.strptime(data_inicio, "%Y-%m-%d").date()
        fim = dt.strptime(data_fim, "%Y-%m-%d").date()
    except (TypeError, ValueError):
        raise ErroReserva(
            'As datas devem estar no formato AAAA-MM-DD.'
        )

    if fim <= inicio:
        raise ErroReserva(
            'A data de fim deve ser posterior à data de início.'
        )

    return inicio, fim

def calcular_orcamento_reserva(veiculo_id, data_inicio, data_fim):
    if not data_inicio or not data_fim:
        raise ErroReserva(
            'As datas de início e fim sao obrigatórias.'
        )

    try:
        inicio = dt.strptime(data_inicio, "%Y-%m-%d").date()
        fim = dt.strptime(data_fim, "%Y-%m-%d").date()
    except (TypeError, ValueError):
        raise ErroReserva(
            'As datas devem estar no formato AAAA-MM-DD.'
        )

    if fim <= inicio:
        raise ErroReserva(
            'A data de fim deve ser posterior À data de início.'
        )
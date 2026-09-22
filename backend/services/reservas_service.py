from datetime import date, datetime as dt
from models import Reserva, Veiculo
from services.veiculos_service import motivo_indisponibilidade

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

def veiculo_disponivel_no_periodo(
        veiculo_id,
        data_inicio,
        data_fim,
        reserva_a_ignorar_id=None
):
    consulta = Reserva.query.filter(
        Reserva.veiculo_id == veiculo_id,
        Reserva. estado == 'Ativa',
        Reserva.data_inicio <= data_fim.isoformat(),
        Reserva.data_fim >= data_inicio.isoformat()
    )

    if reserva_a_ignorar_id is not None:
        consulta = consulta.filter(
            Reserva.id != reserva_a_ignorar_id
        )

    return consulta.first() is None

def calcular_orcamento_reserva(
        veiculo_id,
        data_inicio,
        data_fim,
        reserva_a_ignorar_id=None
):
    data_inicio_obj, data_fim_obj = validar_datas_reserva(
        data_inicio,
        data_fim
    )

    if data_inicio_obj < date.today():
        raise ErroReserva(
            'A data de início não pode ser anterior a hoje.'
        )

    veiculo =Veiculo.query.get(veiculo_id)
    if veiculo is None:
        raise ErroReserva('Veículo não encontrado.', 404)

    # Inativo, em manutenção, inspeção fora de validade ou revisão em atraso
    motivo = motivo_indisponibilidade(veiculo, date.today())
    if motivo:
        raise ErroReserva(
            f'Veículo indisponível para aluguer: {motivo}',
            409
        )

    if not veiculo_disponivel_no_periodo(
        veiculo_id,
        data_inicio_obj,
        data_fim_obj,
        reserva_a_ignorar_id
    ):
        raise ErroReserva(
            'Veículo já tem uma reserva para essas datas.',
            409
        )

    numero_dias = (data_fim_obj - data_inicio_obj).days
    valor_total = veiculo.valor_diaria * numero_dias

    return {
        'veiculo': veiculo,
        'data_inicio': data_inicio_obj,
        'data_fim': data_fim_obj,
        'numero_dias': numero_dias,
        'valor_diaria': veiculo.valor_diaria,
        'valor_total': valor_total,
    }
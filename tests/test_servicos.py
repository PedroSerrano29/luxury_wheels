from datetime import date

import pytest
from models import Veiculo
from services.reservas_service import ErroReserva, validar_datas_reserva
from services.veiculos_service import (
    motivo_indisponibilidade,
    registar_revisao,
    somar_um_ano,
    veiculo_disponivel_para_aluguer,
)

HOJE = date(2026, 9, 21)


def veiculo(**campos):
    base = dict(ativo=True, em_manutencao=False,
                data_ultima_inspecao='2026-03-01', data_proxima_revisao='2027-03-01')
    base.update(campos)
    return Veiculo(**base)


def test_veiculo_em_dia_esta_disponivel():
    assert motivo_indisponibilidade(veiculo(), HOJE) is None
    assert veiculo_disponivel_para_aluguer(veiculo(), HOJE)


def test_inspecao_com_mais_de_um_ano_fica_indisponivel():
    assert motivo_indisponibilidade(veiculo(data_ultima_inspecao='2025-09-20'), HOJE) == 'Inspeção fora de validade.'


def test_inspecao_feita_ha_exatamente_um_ano_ainda_e_valida():
    assert motivo_indisponibilidade(veiculo(data_ultima_inspecao='2025-09-21'), HOJE) is None


def test_revisao_em_atraso_fica_indisponivel():
    assert motivo_indisponibilidade(veiculo(data_proxima_revisao='2026-09-20'), HOJE) == 'Revisão em atraso.'


def test_revisao_marcada_para_hoje_ainda_e_valida():
    assert motivo_indisponibilidade(veiculo(data_proxima_revisao='2026-09-21'), HOJE) is None


def test_em_manutencao_ou_inativo_fica_indisponivel():
    assert motivo_indisponibilidade(veiculo(em_manutencao=True), HOJE) == 'Veículo em manutenção.'
    assert motivo_indisponibilidade(veiculo(ativo=False), HOJE) == 'Veículo inativo.'


def test_sem_datas_fica_indisponivel():
    assert motivo_indisponibilidade(veiculo(data_ultima_inspecao=None), HOJE) == 'Inspeção fora de validade.'
    assert motivo_indisponibilidade(veiculo(data_proxima_revisao=None), HOJE) == 'Revisão em atraso.'


def test_somar_um_ano_trata_29_de_fevereiro():
    assert somar_um_ano(date(2024, 2, 29)) == date(2025, 2, 28)
    assert somar_um_ano(date(2026, 9, 21)) == date(2027, 9, 21)


def test_registar_revisao_calcula_a_proxima():
    v = veiculo(data_proxima_revisao='2026-01-01')
    registar_revisao(v, HOJE)
    assert v.data_ultima_revisao == '2026-09-21'
    assert v.data_proxima_revisao == '2027-09-21'
    assert veiculo_disponivel_para_aluguer(v, HOJE)


def test_datas_de_reserva_invalidas_sao_recusadas():
    with pytest.raises(ErroReserva):
        validar_datas_reserva('2026-10-05', '2026-10-01')   # fim antes do início
    with pytest.raises(ErroReserva):
        validar_datas_reserva('05/10/2026', '10/10/2026')   # formato errado
    with pytest.raises(ErroReserva):
        validar_datas_reserva(None, '2026-10-01')           # data em falta

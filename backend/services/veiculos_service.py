from datetime import datetime as dt

# Regras de disponibilidade e manutenção dos veículos.
# Recebem a data de referência em vez de usar date.today(), para serem testáveis.

def texto_para_data(texto):
    return dt.strptime(texto, "%Y-%m-%d").date()

def somar_um_ano(data):
    try:
        return data.replace(year=data.year + 1)
    except ValueError:  # 29 de fevereiro num ano não bissexto
        return data.replace(year=data.year + 1, day=28)

def motivo_indisponibilidade(veiculo, data_referencia):
    """Devolve o motivo pelo qual o veículo não pode ser alugado, ou None se pode."""
    if not veiculo.ativo:
        return 'Veículo inativo.'
    if veiculo.em_manutencao:
        return 'Veículo em manutenção.'

    # Sem data não há garantia de que está legal: fica indisponível
    inspecao = veiculo.data_ultima_inspecao
    if not inspecao or somar_um_ano(texto_para_data(inspecao)) < data_referencia:
        return 'Inspeção fora de validade.'

    revisao = veiculo.data_proxima_revisao
    if not revisao or texto_para_data(revisao) < data_referencia:
        return 'Revisão em atraso.'

    return None

def veiculo_disponivel_para_aluguer(veiculo, data_referencia):
    return motivo_indisponibilidade(veiculo, data_referencia) is None

# Registo de manutenção; quem chama faz o commit
def registar_inspecao(veiculo, data_inspecao):
    veiculo.data_ultima_inspecao = data_inspecao.isoformat()

def registar_revisao(veiculo, data_revisao):
    veiculo.data_ultima_revisao = data_revisao.isoformat()
    veiculo.data_proxima_revisao = somar_um_ano(data_revisao).isoformat()
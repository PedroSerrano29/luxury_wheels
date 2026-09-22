from conftest import dia


def reservar(client, token, veiculo_id, inicio, fim):
    return client.post('/api/reservas', headers={'Authorization': token}, json={
        'veiculo_id': veiculo_id,
        'data_inicio': inicio,
        'data_fim': fim,
        'forma_pagamento_tipo': 'Cartão',
    })


# --- Veículos ---

def test_listagem_so_mostra_veiculos_disponiveis(client):
    veiculos = client.get('/api/veiculos').get_json()
    assert [v['modelo'] for v in veiculos] == ['Series 3']


def test_pesquisa_por_marca_e_modelo(client):
    assert len(client.get('/api/veiculos?pesquisa=bmw series').get_json()) == 1
    assert len(client.get('/api/veiculos?pesquisa=SERIES').get_json()) == 1
    assert client.get('/api/veiculos?pesquisa=xyz').get_json() == []


def test_valor_maximo_invalido_devolve_400(client):
    assert client.get('/api/veiculos?valor_maximo=abc').status_code == 400


def test_detalhe_indica_o_motivo_da_indisponibilidade(client):
    assert client.get('/api/veiculos/1').get_json()['motivo_indisponibilidade'] is None
    assert client.get('/api/veiculos/2').get_json()['motivo_indisponibilidade'] == 'Inspeção fora de validade.'
    assert client.get('/api/veiculos/3').get_json()['motivo_indisponibilidade'] == 'Revisão em atraso.'


# --- Orçamento e reservas ---

def test_orcamento_calcula_valor_total(client):
    resposta = client.get(f'/api/reservas/orcamento?veiculo_id=1&data_inicio={dia(1)}&data_fim={dia(4)}')
    assert resposta.status_code == 200
    assert resposta.get_json() == {'numero_dias': 3, 'valor_diaria': 85.0, 'valor_total': 255.0}


def test_criar_reserva_grava_o_valor_total(client, token):
    resposta = reservar(client, token, 1, dia(1), dia(4))
    assert resposta.status_code == 201
    assert resposta.get_json()['valor_total'] == 255.0


def test_reserva_sobreposta_e_recusada(client, token):
    reservar(client, token, 1, dia(1), dia(4))
    resposta = reservar(client, token, 1, dia(3), dia(6))
    assert resposta.status_code == 409


def test_reserva_de_veiculo_indisponivel_e_recusada(client, token):
    resposta = reservar(client, token, 2, dia(1), dia(4))
    assert resposta.status_code == 409
    assert 'Inspeção fora de validade' in resposta.get_json()['erro']


def test_reserva_no_passado_e_recusada(client, token):
    assert reservar(client, token, 1, dia(-2), dia(2)).status_code == 400


def test_reserva_sem_token_e_recusada(client):
    assert reservar(client, '', 1, dia(1), dia(4)).status_code == 401


def test_alterar_data_fim_recalcula_o_valor(client, token):
    reserva_id = reservar(client, token, 1, dia(1), dia(4)).get_json()['id']
    resposta = client.put(f'/api/reservas/{reserva_id}', headers={'Authorization': token},
                          json={'data_fim': dia(5)})
    assert resposta.status_code == 200
    assert resposta.get_json()['novo_valor_total'] == 340.0


def test_nao_se_cancela_uma_reserva_ja_a_decorrer(client, token):
    reserva_id = reservar(client, token, 1, dia(0), dia(3)).get_json()['id']   # começa hoje: Ativa
    resposta = client.put(f'/api/reservas/{reserva_id}', headers={'Authorization': token},
                          json={'cancelar': True})
    assert resposta.status_code == 409


# --- Registo ---

def test_registo_sem_password_devolve_400(client):
    resposta = client.post('/api/auth/registo', json={'nome': 'Ana', 'email': 'ana@teste.pt'})
    assert resposta.status_code == 400


def test_registo_com_email_repetido_e_recusado(client, token):
    resposta = client.post('/api/auth/registo', json={
        'nome': 'Outro', 'email': 'cliente@teste.pt',
        'password': 'segredo123', 'password_confirm': 'segredo123',
    })
    assert resposta.status_code == 400

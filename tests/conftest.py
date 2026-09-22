import os
import sys
from datetime import date, timedelta

# A app lê a SECRET_KEY do ambiente; nos testes não é preciso o .env
os.environ.setdefault('SECRET_KEY', 'chave-apenas-para-testes-com-32-bytes-ou-mais')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

import pytest
from app import create_app
from config import Config
from models import db, Veiculo


def criar_veiculo(marca, modelo, dias_desde_inspecao, dias_ate_revisao, valor_diaria=85.0):
    hoje = date.today()
    return Veiculo(
        marca=marca,
        modelo=modelo,
        categoria='Grande',
        transmissao='Automática',
        tipo='Carro',
        capacidade_pessoas=5,
        valor_diaria=valor_diaria,
        data_ultima_inspecao=(hoje - timedelta(days=dias_desde_inspecao)).isoformat(),
        data_proxima_revisao=(hoje + timedelta(days=dias_ate_revisao)).isoformat(),
    )


@pytest.fixture
def app(tmp_path):
    # Base de dados própria para cada teste, num ficheiro temporário
    class ConfigTeste(Config):
        TESTING = True
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{tmp_path / 'teste.db'}"

    app = create_app(ConfigTeste)
    with app.app_context():
        db.create_all()
        db.session.add_all([
            criar_veiculo('BMW', 'Series 3', dias_desde_inspecao=30, dias_ate_revisao=180),   # id 1, disponível
            criar_veiculo('Fiat', 'Panda', dias_desde_inspecao=400, dias_ate_revisao=180),    # id 2, inspeção fora de validade
            criar_veiculo('Opel', 'Corsa', dias_desde_inspecao=30, dias_ate_revisao=-1),      # id 3, revisão em atraso
        ])
        db.session.commit()
        yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def token(client):
    client.post('/api/auth/registo', json={
        'nome': 'Cliente Teste',
        'email': 'cliente@teste.pt',
        'password': 'segredo123',
        'password_confirm': 'segredo123',
    })
    resposta = client.post('/api/auth/login', json={'email': 'cliente@teste.pt', 'password': 'segredo123'})
    return resposta.get_json()['token']


def dia(deslocamento):
    """Data em texto, relativa a hoje (ex: dia(1) é amanhã)."""
    return (date.today() + timedelta(days=deslocamento)).isoformat()

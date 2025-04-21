import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date
import os

from setup_database import Base, Veiculo, Cliente, Reserva, FormaPagamento

# Caminho relativo para a base de dados
db_path = os.path.join(os.path.dirname(__file__), '../database/luxury_wheels.db')
engine = create_engine(f'sqlite:///{db_path}')
Session = sessionmaker(bind=engine)
session = Session()

# --- Populando a tabela Veiculo a partir de CSV ---
csv_path = os.path.join(os.path.dirname(__file__), '../database/veiculos.csv')

with open(csv_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        veiculo = Veiculo(
            marca=row['marca'],
            modelo=row['modelo'],
            matricula=row['matricula'],
            combustivel=row['combustivel'],
            categoria=row['categoria'],
            transmissao=row['transmissao'],
            tipo=row['tipo'],
            lugares=int(row['lugares']),
            imagem=row['imagem'],
            diaria=float(row['diaria']),
            disponivel=row['disponivel'].lower() == 'true',
            ultima_revisao=date.fromisoformat(row['ultima_revisao']),
            proxima_revisao=date.fromisoformat(row['proxima_revisao']),
            ultima_inspecao=date.fromisoformat(row['ultima_inspecao'])
        )
        session.add(veiculo)

# --- Populando a tabela Cliente ---
nomes = ['João Silva', 'Maria Oliveira', 'Pedro Santos', 'Ana Costa']
emails_base = ['joao@example.com', 'maria@example.com', 'pedro@example.com', 'ana@example.com']

for i, (nome, email_base) in enumerate(zip(nomes, emails_base)):
    email = f"{email_base.split('@')[0]}{i}@{email_base.split('@')[1]}"
    cliente_existente = session.query(Cliente).filter_by(email=email).first()
    if not cliente_existente:
        cliente = Cliente(
            nome=nome,
            email=email
        )
        cliente.set_password('senha123')
        session.add(cliente)

# --- Populando a tabela FormaPagamento ---
formas_pagamento = ['Cartão de Crédito', 'PayPal', 'Transferência Bancária']
for tipo in formas_pagamento:
    forma_pagamento = FormaPagamento(tipo=tipo)
    session.add(forma_pagamento)

# Commit das alterações
session.commit()

# --- Populando a tabela Reserva ---
import random
from datetime import timedelta

clientes = session.query(Cliente).all()
veiculos = session.query(Veiculo).all()

for _ in range(10):
    reserva = Reserva(
        cliente_id=random.choice(clientes).id,
        veiculo_id=random.choice(veiculos).id,
        data_inicio=date.today() - timedelta(days=random.randint(1, 30)),
        data_fim=date.today() + timedelta(days=random.randint(1, 30)),
        valor_total=round(random.uniform(100, 1000))
    )
    session.add(reserva)

# Commit final
session.commit()

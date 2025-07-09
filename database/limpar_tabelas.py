from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import sys

# Caminho absoluto para a base de dados
db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'luxury_wheels.db'))
engine = create_engine(f'sqlite:///{db_path}')
Session = sessionmaker(bind=engine)
session = Session()

# Adiciona o diretório da base do projeto ao sys.path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from setup_database import Veiculo, Cliente, Reserva, FormaPagamento

def limpar_tabelas():
    session.query(Veiculo).delete()
    session.query(Cliente).delete()
    session.query(Reserva).delete()
    session.query(FormaPagamento).delete()
    session.commit()

limpar_tabelas()
print("Conteúdo das tabelas foi limpo com sucesso.")

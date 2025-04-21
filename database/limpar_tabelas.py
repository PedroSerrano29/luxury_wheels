from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Caminho relativo para a base de dados
db_path = os.path.join(os.path.dirname(__file__), '../database/luxury_wheels.db')
engine = create_engine(f'sqlite:///{db_path}')
Session = sessionmaker(bind=engine)
session = Session()

# Importar as classes do arquivo principal
from setup_database import Veiculo, Cliente, Reserva, FormaPagamento

# Função para limpar o conteúdo das tabelas
def limpar_tabelas():
    session.query(Veiculo).delete()
    session.query(Cliente).delete()
    session.query(Reserva).delete()
    session.query(FormaPagamento).delete()
    session.commit()

# Chamar a função para limpar as tabelas
limpar_tabelas()

print("Conteúdo das tabelas foi limpo com sucesso.")

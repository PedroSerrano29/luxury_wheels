from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, Date, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker
import hashlib
import os

Base = declarative_base()

class Veiculo(Base):
    __tablename__ = 'veiculos'
    id = Column(Integer, primary_key=True)
    marca = Column(String, nullable=False)
    modelo = Column(String, nullable=False)
    matricula = Column(String)
    combustivel = Column(String)
    categoria = Column(String)
    transmissao = Column(String)
    tipo = Column(String)
    lugares = Column(Integer)
    imagem = Column(String)
    diaria = Column(Float)
    disponivel = Column(Boolean, default=True)
    ultima_revisao = Column(Date)
    proxima_revisao = Column(Date)
    ultima_inspecao = Column(Date)


class Cliente(Base):
    __tablename__ = 'clientes'
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    senha = Column(String, nullable=False)

    # Para usar werkzeug.security, descomente as linhas abaixo:
    # def set_password(self, password):
    #     self.senha = generate_password_hash(password)
    #
    # def check_password(self, password):
    #     return check_password_hash(self.senha, password)

    # Para usar hashlib (sem werkzeug.security), use as funções abaixo:
    def set_password(self, password):
        salt = os.urandom(16).hex()
        pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000).hex()
        self.senha = f"{salt}${pwd_hash}"

    def check_password(self, password):
        try:
            salt, pwd_hash = self.senha.split('$')
            check_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000).hex()
            return check_hash == pwd_hash
        except Exception:
            return False


class Reserva(Base):
    __tablename__ = 'reservas'
    id = Column(Integer, primary_key=True)
    cliente_id = Column(Integer, ForeignKey('clientes.id'))
    veiculo_id = Column(Integer, ForeignKey('veiculos.id'))
    data_inicio = Column(Date)
    data_fim = Column(Date)
    valor_total = Column(Float)

class FormaPagamento(Base):
    __tablename__ = 'formas_pagamento'
    id = Column(Integer, primary_key=True)
    tipo = Column(String, nullable=False)

# Caminho relativo para a base de dados
db_path = os.path.join(os.path.dirname(__file__), '../database/luxury_wheels.db')
engine = create_engine(f'sqlite:///{db_path}')
Base.metadata.create_all(engine)


# Configuração da sessão
Session = sessionmaker(bind=engine)
session = Session()

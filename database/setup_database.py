from sqlalchemy import create_engine, Column, Integer, String, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash

import os

Base = declarative_base()

class Cliente(Base):
    __tablename__ = 'clientes'
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    senha = Column(String, nullable=False)

    def set_password(self, password):
        self.senha = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.senha, password)

class FormaPagamento(Base):
    __tablename__ = 'formas_pagamento'
    id = Column(Integer, primary_key=True)
    tipo = Column(String, nullable=False)

class Veiculo(Base):
    __tablename__ = 'veiculos'
    id = Column(Integer, primary_key=True)
    marca = Column(String, nullable=False)
    modelo = Column(String, nullable=False)
    categoria = Column(String, nullable=False)
    transmissao = Column(String, nullable=False)
    tipo = Column(String, nullable=False)
    lugares = Column(Integer, nullable=False)
    diaria = Column(Integer, nullable=False)
    imagem = Column(String)
    disponivel = Column(Boolean, default=True)
    ultima_inspecao = Column(Date)
    proxima_revisao = Column(Date)

class Reserva(Base):
    __tablename__ = 'reservas'
    id = Column(Integer, primary_key=True)
    veiculo_id = Column(Integer, nullable=False)
    cliente_email = Column(String, nullable=False)
    data_inicio = Column(Date, nullable=False)
    data_fim = Column(Date, nullable=False)

# Caminho relativo para a base de dados
db_path = os.path.join(os.path.dirname(__file__), '../database/luxury_wheels.db')
engine = create_engine(f'sqlite:///{db_path}')
Base.metadata.create_all(engine)

# Configuração da sessão
Session = sessionmaker(bind=engine)
session = Session()

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Veiculo(db.Model):
    __tablename__ = 'veiculos'

    id = db.Column(db.Integer, primary_key=True)
    marca = db.Column(db.String, nullable=False)
    modelo = db.Column(db.String, nullable=False)
    categoria = db.Column(db.String, nullable=False)
    transmissao = db.Column(db.String, nullable=False)
    tipo = db.Column(db.String, nullable=False)
    capacidade_pessoas = db.Column(db.Integer, nullable=False)
    valor_diaria = db.Column(db.Float, nullable=False)
    imagem_url = db.Column(db.String)
    data_ultima_revisao = db.Column(db.String)
    data_proxima_revisao = db.Column(db.String)
    data_ultima_inspecao = db.Column(db.String)
    disponivel = db.Column(db.Boolean, nullable=False, default=True)
    em_manutencao = db.Column(db.Boolean, nullable=False, default=False)

class Cliente(db.Model):
	__tablename__ = 'clientes'
	
	id = db.Column(db.Integer, primary_key=True)
	nome = db.Column(db.String, nullable=False)
	email = db.Column(db.String, nullable=False, unique=True)
	password_hash = db.Column(db.String, nullable=False)
	data_registo = db.Column(db.String, nullable=False, server_default=db.func.current_timestamp())
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Veiculo(db.Model):
    __tablename__ = 'veiculos'

    id = db.Column(db.Integer, primary_key=True)
    marca = db.Column(db.String, nullable=False)
    modelo = db.Column(db.String, nullable=False)
    matricula = db.Column(db.String)
    combustivel = db.Column(db.String)
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
    ativo = db.Column(db.Boolean, nullable=False, default=True)

    def to_dict(self):
        return {
            "id": self.id,
            "marca": self.marca,
            "modelo": self.modelo,
            "matricula": self.matricula,
            "combustivel": self.combustivel,
            "categoria": self.categoria,
            "transmissao": self.transmissao,
            "tipo": self.tipo,
            "capacidade_pessoas": self.capacidade_pessoas,
            "valor_diaria": self.valor_diaria,
            "imagem_url": self.imagem_url,
            "data_ultima_revisao": self.data_ultima_revisao,
            "data_proxima_revisao": self.data_proxima_revisao,
            "data_ultima_inspecao": self.data_ultima_inspecao,
            "disponivel": self.disponivel,
            "em_manutencao": self.em_manutencao,
            "ativo": self.ativo
        }

class Cliente(db.Model):
	__tablename__ = 'clientes'
	
	id = db.Column(db.Integer, primary_key=True)
	nome = db.Column(db.String, nullable=False)
	email = db.Column(db.String, nullable=False, unique=True)
	password_hash = db.Column(db.String, nullable=False)
	data_registo = db.Column(db.String, nullable=False, server_default=db.func.current_timestamp())

class FormaPagamento(db.Model):
    __tablename__ = 'formas_pagamento'

    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    tipo = db.Column(db.String, nullable=False)
    detalhes = db.Column(db.String)

class Reserva(db.Model):
    __tablename__ = 'reservas'

    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    veiculo_id = db.Column(db.Integer, db.ForeignKey('veiculos.id'), nullable=False)
    data_inicio = db.Column(db.String, nullable=False)
    data_fim = db.Column(db.String, nullable=False)
    valor_total = db.Column(db.Float, nullable=False)
    forma_pagamento_id = db.Column(db.Integer, db.ForeignKey('formas_pagamento.id'), nullable=False)
    estado = db.Column(db.String, nullable=False, default='Ativa')  # 'Ativa','Cancelada','Concluída'
    data_criacao = db.Column(db.String, nullable=False, server_default=db.func.current_timestamp())

    cliente = db.relationship('Cliente')
    veiculo = db.relationship('Veiculo')
    forma_pagamento = db.relationship('FormaPagamento')

class Utilizador(db.Model):
    __tablename__ = 'utilizadores'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password_hash = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False, default='gestor')  # 'gestor', 'admin'
    data_criacao = db.Column(db.String, nullable=False, server_default=db.func.current_timestamp())
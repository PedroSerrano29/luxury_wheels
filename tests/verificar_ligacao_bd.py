import os
from flask import Flask
from models import db, Veiculo, Cliente, FormaPagamento, Reserva, Utilizador

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, '..', 'database', 'luxury_wheels.db')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'

db.init_app(app)

with app.app_context():
    veiculos = Veiculo.query.all()
    print(f"Encontrei {len(veiculos)} veículos na base de dados.")
    for v in veiculos[:3]:
        print(f" - {v.marca} {v.modelo} ({v.categoria}) — {v.valor_diaria}€/dia")
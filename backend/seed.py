import os
import csv
from flask import Flask
from models import db, Veiculo

""" # Codigo para testar a leitura do arquivo CSV
with open('../database/veiculos.csv', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for linha in reader:
        print(linha)
"""

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, '..', 'database', 'luxury_wheels.db')
CSV_PATH = os.path.join(BASE_DIR, '..', 'database', 'veiculos.csv')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =f'sqlite:///{DB_PATH}'
db.init_app(app)

def mapear_categoria(categoria_original, tipo_original, diaria):
    if tipo_original == 'Moto':
        return categoria_original # Naked, Scooter, Touring, Moto — mantém-se tal como está

    # A partir daqui, só carros
    if categoria_original == 'SUV':
        return 'SUV'
    if float(diaria) >= 90:
        return 'Luxo'

    mapa_carros = {
        'Citadino': 'Pequeno',
        'Compacto': 'Médio',
        'Berline': 'Grande',
    }
    return mapa_carros.get(categoria_original, categoria_original)  # Retorna a categoria original se não estiver no mapa

def mapear_tipo(tipo_original):
    return 'Carro' if tipo_original == 'Automóvel' else 'Moto'

def mapear_transmissao(transmissao_original, categoria_original, tipo_original):
    if tipo_original == 'Moto':
        return 'Automática' if categoria_original == 'Scooter' else 'Manual'
    return transmissao_original  # Para carros, mantém a transmissão original

def mapear_disponivel(disponivel_original):
    return disponivel_original == 'TRUE'

with app.app_context():
    with open(CSV_PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for linha in reader:
            veiculo = Veiculo(
                marca=linha['marca'],
                modelo=linha['modelo'],
                matricula=linha['matricula'],
                combustivel=linha['combustivel'],
                categoria=mapear_categoria(linha['categoria'], linha['tipo'], linha['diaria']),
                transmissao=mapear_transmissao(linha['transmissao'], linha['categoria'], linha['tipo']),
                tipo=mapear_tipo(linha['tipo']),
                capacidade_pessoas=int(linha['lugares']),
                valor_diaria=float(linha['diaria']),
                imagem_url=linha['imagem'],
                data_ultima_revisao=linha['ultima_revisao'],
                data_proxima_revisao=linha['proxima_revisao'],
                data_ultima_inspecao=linha['ultima_inspecao'],
                disponivel=mapear_disponivel(linha['disponivel']),
            )
            db.session.add(veiculo)

    db.session.commit()
    print(f"Importados {Veiculo.query.count()} veículos.")
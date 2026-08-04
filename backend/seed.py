import csv

with open('../database/veiculos.csv', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for linha in reader:
        print(linha)

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
    return True if disponivel_original == 'TRUE' else False
import csv

with open('../database/veiculos.csv', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for linha in reader:
        print(linha)
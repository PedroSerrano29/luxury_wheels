CREATE TABLE veiculos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    marca TEXT NOT NULL,
    modelo TEXT NOT NULL,
    categoria TEXT NOT NULL,        -- 'Pequeno', 'Médio', 'Grande', 'SUV', 'Luxo'
    transmissao TEXT NOT NULL,      -- 'Automático', 'Manual'
    tipo TEXT NOT NULL,             -- 'Carro', 'Moto'
    capacidade_pessoas INTEGER NOT NULL,
    valor_diaria REAL NOT NULL,
    imagem_url TEXT,
    data_ultima_revisao TEXT,
    data_proxima_revisao TEXT,
    data_ultima_inspecao TEXT,
    disponivel BOOLEAN NOT NULL DEFAULT 1,
    em_manutencao BOOLEAN NOT NULL DEFAULT 0
);
CREATE TABLE clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    data_registo TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE formas_pagamento (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER NOT NULL,
    tipo TEXT NOT NULL,
    detalhes TEXT,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
);

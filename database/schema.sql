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
    tipo TEXT NOT NULL,        -- 'MB WAY', 'Cartão'
    detalhes TEXT,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
);
CREATE TABLE reservas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER NOT NULL,
    veiculo_id INTEGER NOT NULL,
    data_inicio TEXT NOT NULL,
    data_fim TEXT NOT NULL ,
    valor_total REAL NOT NULL,
    forma_pagamento_id INTEGER NOT NULL,
    estado TEXT NOT NULL DEFAULT 'Ativa',      -- 'Ativa','Cancelada','Concluída'
    data_criacao TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id),
    FOREIGN KEY (veiculo_id) REFERENCES veiculos(id),
    FOREIGN KEY (forma_pagamento_id) REFERENCES formas_pagamento(id)
);
CREATE TABLE utilizadores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'gestor',  -- 'gestor', 'admin'
    data_criacao TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE veiculos ADD COLUMN matricula TEXT;
CREATE UNIQUE INDEX idx_veiculos_matricula ON veiculos(matricula);
ALTER TABLE veiculos ADD COLUMN combustivel TEXT;  
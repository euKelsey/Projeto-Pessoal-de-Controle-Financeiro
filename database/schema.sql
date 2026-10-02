PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS categoria (
    id INTEGER PRIMARY KEY,
    nome TEXT NOT NULL,
    tipo TEXT NOT NULL,
    descricao TEXT,
    status TEXT NOT NULL DEFAULT 'ATIVA',

    CHECK (tipo IN ('RECEITA', 'DESPESA')),
    CHECK (status IN ('ATIVA', 'INATIVA')),

    UNIQUE (nome, tipo)
);
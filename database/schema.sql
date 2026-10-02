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

CREATE TABLE IF NOT EXISTS cartao (
    id INTEGER PRIMARY KEY,
    nome TEXT NOT NULL,
    instituicao TEXT NOT NULL,
    limite_total INTEGER NOT NULL,
    dia_fechamento INTEGER NOT NULL,
    dia_vencimento INTEGER NOT NULL,
    status TEXT NOT NULL DEFAULT 'ATIVO',
    observacao TEXT,

    CHECK (limite_total >= 0),
    CHECK (dia_fechamento BETWEEN 1 AND 31),
    CHECK (dia_vencimento BETWEEN 1 AND 31),
    CHECK (status IN ('ATIVO', 'INATIVO'))
);

CREATE TABLE IF NOT EXISTS recorrencia (
    id INTEGER PRIMARY KEY,
    tipo_lancamento TEXT NOT NULL,
    descricao TEXT NOT NULL,
    valor INTEGER NOT NULL,
    categoria_id INTEGER NOT NULL,
    periodicidade TEXT NOT NULL,
    data_inicio TEXT NOT NULL,
    data_fim TEXT,
    dia_referencia INTEGER,
    destino_geracao TEXT NOT NULL DEFAULT 'LANCAMENTO',
    cartao_id INTEGER,
    status TEXT NOT NULL DEFAULT 'ATIVA',
    observacao TEXT,

    CHECK (tipo_lancamento IN ('RECEITA', 'DESPESA')),
    CHECK (valor > 0),
    CHECK (periodicidade IN ('MENSAL', 'SEMANAL', 'QUINZENAL', 'ANUAL')),
    CHECK (dia_referencia IS NULL OR dia_referencia BETWEEN 1 AND 31),
    CHECK (destino_geracao IN ('LANCAMENTO', 'COMPRA_CARTAO')),
    CHECK (status IN ('ATIVA', 'PAUSADA', 'ENCERRADA')),
    CHECK (data_fim IS NULL OR data_fim >= data_inicio),

    FOREIGN KEY (categoria_id)
        REFERENCES categoria(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    FOREIGN KEY (cartao_id)
        REFERENCES categoria(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);
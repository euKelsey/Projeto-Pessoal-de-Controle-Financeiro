import sqlite3
from pathlib import Path

PASTA_DATABASE = Path(__file__).parent

CAMINHO_SCHEMA = PASTA_DATABASE / "schema.sql"
CAMINHO_BANCO = PASTA_DATABASE / "controle_financeiro_teste.db"

if CAMINHO_BANCO.exists():
    CAMINHO_BANCO.unlink()

conexao = sqlite3.connect(CAMINHO_BANCO)

conexao.execute("PRAGMA foreign_keys = ON;")

with open(CAMINHO_SCHEMA, "r",
encoding="utf-8") as arquivo:
    schema = arquivo.read()
    
conexao.executescript(schema)

conexao.commit()
conexao.close()

print("Banco criado e schema executado com sucesso.")

conexao = sqlite3.connect(CAMINHO_BANCO)
conexao.execute("PRAGMA foreign_keys = ON;")

cursor = conexao.cursor()

cursor.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type = 'table';
""")

tabelas = cursor.fetchall()

print("Tabelas encontradas:")
print(tabelas)

cursor.execute("""
    INSERT INTO categoria (nome, tipo, descricao)
    VALUES (?, ?, ?);
""", ("Alimentação", "DESPESA", "Gastos com alimentação"))

conexao.commit()

cursor.execute("""
    SELECT id, nome, tipo, descricao, status
    FROM categoria;
""")

categorias = cursor.fetchall()

print("Categorias cadastradas")

try:
    cursor.execute("""
        INSERT INTO categoria (nome, tipo, descricao)
        VALUES (?, ?, ?);
    """, ("Teste inválido", "OUTRO", "Categoria para teste CHECK"))
    
    conexao.commit()
    
except sqlite3.IntegrityError as erro:
    print("Erro esperado ao testar tipo inválido:")
    print(erro)
    
try:
    cursor.execute("""
        INSERT INTO categoria (nome, tipo, descricao, status)
        VALUES (?, ?, ?, ?);
    """, ("Teste status", "DESPESA", "Teste de status inválido", "BLOQUEADA"))

    conexao.commit()

except sqlite3.IntegrityError as erro:
    print("Erro esperado ao testar status inválido:")
    print(erro)
    
try:
    cursor.execute("""
        INSERT INTO categoria (nome, tipo, descricao)
        VALUES (?, ?, ?);
    """, (None, "DESPESA", "Teste de nome obrigatório"))

    conexao.commit()

except sqlite3.IntegrityError as erro:
    print("Erro esperado ao testar nome obrigatório:")
    print(erro)
    
cursor.execute("""
    SELECT id, nome, tipo, descricao, status
    FROM categoria;
""")

categorias = cursor.fetchall()

print("Categorias existentes após os testes:")

for categoria in categorias:
    print(categoria)

try:
    cursor.execute("""
        INSERT INTO cartao (
            nome,
            instituicao,
            limite_total,
            dia_fechamento,
            dia_vencimento,
            observacao
        )
        VALUES (?, ?, ?, ?, ?, ?);
    """, (
        "Nubank Principal",
        "Nubank",
        500000,
        2,
        10,
        "Cartão principal"
    ))

    conexao.commit()

except sqlite3.IntegrityError as erro:
    print("Erro ao cadastrar cartão:")
    print(erro)
    
cursor.execute("""
    SELECT
        id,
        nome,
        instituicao,
        limite_total,
        dia_fechamento,
        dia_vencimento,
        status,
        observacao
    FROM cartao;
""")

cartoes = cursor.fetchall()

print("Cartões cadastrados:")

for cartao in cartoes:
    print(cartao)
    
try:
    cursor.execute("""
        INSERT INTO recorrencia (
            tipo_lancamento,
            descricao,
            valor,
            categoria_id,
            periodicidade,
            data_inicio,
            dia_referencia,
            destino_geracao,
            status,
            observacao
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, (
        "DESPESA",
        "Internet",
        18300,
        1,
        "MENSAL",
        "2026-10-01",
        10,
        "LANCAMENTO",
        "ATIVA",
        "Conta de internet mensal"
    ))

    conexao.commit()

except sqlite3.IntegrityError as erro:
    print("Erro ao cadastrar recorrência válida:")
    print(erro)
    
cursor.execute("""
    SELECT
        id,
        tipo_lancamento,
        descricao,
        valor,
        categoria_id,
        periodicidade,
        data_inicio,
        data_fim,
        dia_referencia,
        destino_geracao,
        cartao_id,
        status,
        observacao
    FROM recorrencia;
""")

recorrencias = cursor.fetchall()

print("Recorrências cadastradas:")

for recorrencia in recorrencias:
    print(recorrencia)
    
try:
    cursor.execute("""
        INSERT INTO recorrencia (
            tipo_lancamento,
            descricao,
            valor,
            categoria_id,
            periodicidade,
            data_inicio,
            dia_referencia,
            destino_geracao,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, (
        "DESPESA",
        "Teste FK inválida",
        10000,
        999,
        "MENSAL",
        "2026-10-01",
        5,
        "LANCAMENTO",
        "ATIVA"
    ))

    conexao.commit()

except sqlite3.IntegrityError as erro:
    print("Erro esperado ao testar categoria inexistente:")
    print(erro)
    
try:
    cursor.execute("""
        INSERT INTO recorrencia (
            tipo_lancamento,
            descricao,
            valor,
            categoria_id,
            periodicidade,
            data_inicio,
            dia_referencia,
            destino_geracao,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, (
        "DESPESA",
        "Teste dia inválido",
        10000,
        1,
        "MENSAL",
        "2026-10-01",
        40,
        "LANCAMENTO",
        "ATIVA"
    ))
    
    conexao.commit()
    
except sqlite3.IntegrityError as erro:
    print("Erro esperado ao testar dia de referência inválida?:")
    print(erro)
    
try:
    cursor.execute("""
        INSERT INTO recorrencia (
            tipo_lancamento,
            descricao,
            valor,
            categoria_id,
            periodicidade,
            data_inicio,
            dia_referencia,
            destino_geracao,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, (
        "DESPESA",
        "Teste periodicidade inválida",
        10000,
        1,
        "BIMESTRAL",
        "2026-10-01",
        10,
        "LANCAMENTO",
        "ATIVA"
    ))

    conexao.commit()

except sqlite3.IntegrityError as erro:
    print("Erro esperado ao testar periodicidade inválida:")
    print(erro)
    
try:
    cursor.execute("""
        INSERT INTO recorrencia (
            tipo_lancamento,
            descricao,
            valor,
            categoria_id,
            periodicidade,
            data_inicio,
            data_fim,
            dia_referencia,
            destino_geracao,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, (
        "DESPESA",
        "Teste data inválida",
        10000,
        1,
        "MENSAL",
        "2026-10-01",
        "2026-09-01",
        10,
        "LANCAMENTO",
        "ATIVA"
    ))

    conexao.commit()

except sqlite3.IntegrityError as erro:
    print("Erro esperado ao testar data final anterior à inicial:")
    print(erro)
    
try:
    cursor.execute("""
        INSERT INTO recorrencia (
            tipo_lancamento,
            descricao,
            valor,
            categoria_id,
            periodicidade,
            data_inicio,
            dia_referencia,
            destino_geracao,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, (
        "DESPESA",
        "Teste status inválido",
        10000,
        1,
        "MENSAL",
        "2026-10-01",
        10,
        "LANCAMENTO",
        "CANCELADA"
    ))

    conexao.commit()

except sqlite3.IntegrityError as erro:
    print("Erro esperado ao testar status inválido:")
    print(erro)
    
conexao.close()
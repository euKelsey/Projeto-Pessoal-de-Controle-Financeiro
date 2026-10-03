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
    
cursor.execute("""
    INSERT INTO fatura (
        cartao_id,
        mes_referencia,
        data_fechamento,
        data_vencimento,
        status
    )
    VALUES (?, ?, ?, ?, ?);
""", (
    1,
    "2026-10",
    "2026-10-02",
    "2026-10-10",
    "ABERTA"
))

conexao.commit()

print("Fatura válida cadastrada com sucesso.")

cursor.execute("SELECT * FROM fatura;")

print("Faturas cadastradas:")

for fatura in cursor.fetchall():
    print(fatura)
    
try:
    cursor.execute("""
        INSERT INTO fatura (
            cartao_id,
            mes_referencia,
            data_fechamento,
            data_vencimento,
            status
        )
        VALUES (?, ?, ?, ?, ?);
    """, (
        "999",
        "2026-11",
        "2026-11-02",
        "2026-11-10",
        "ABERTA"
    ))
    
    conexao.commit()
    
except sqlite3.IntegrityError as erro:
    print("Erro esperado as testar cartão inexistente: ")
    print(erro)
    
try:
    cursor.execute("""
        INSERT INTO fatura (
            cartao_id,
            mes_referencia,
            data_fechamento,
            data_vencimento,
            status
        )
        VALUES (?, ?, ?, ?, ?);
    """, (
        1,
        "2026-11",
        "2026-11-02",
        "2026-11-10",
        "CANCELADA"
    ))
    
    conexao.commit()
    
except sqlite3.IntegrityError as erro:
    print("Erro esperado as testar STATUS INVALIDO: ")
    print(erro)
    
try:
    cursor.execute("""
        INSERT INTO fatura (
            cartao_id,
            mes_referencia,
            data_fechamento,
            data_vencimento,
            status
        )
        VALUES (?, ?, ?, ?, ?);
    """, (
        1,
        "2026-11",
        "2026-11-02",
        "2026-11-10",
        "ABERTA"
    ))
    
    conexao.commit()
    
except sqlite3.IntegrityError as erro:
    print("Erro esperado as testar STATUS INVALIDO: ")
    print(erro)
    
try:
    cursor.execute("""
        INSERT INTO fatura (
            cartao_id,
            mes_referencia,
            data_fechamento,
            data_vencimento,
            status
        )
        VALUES (?, ?, ?, ?, ?);
    """, (
        1,
        "2026-10",
        "2026-10-03",
        "2026-10-12",
        "FECHADA"
    ))

    conexao.commit()

except sqlite3.IntegrityError as erro:
    print("Erro esperado ao testar fatura duplicada:")
    print(erro)
    
cursor.execute("""
    INSERT INTO lancamento (
        tipo,
        descricao,
        valor_previsto,
        data_prevista,
        categoria_id,
        status,
        origem
    )
    VALUES (?, ?, ?, ?, ?, ?, ?);
""", (
    "DESPESA",
    "Supermercado",
    25000,
    "2026-10-05",
    1,
    "PENDENTE",
    "MANUAL"
))

conexao.commit()

print("Lançamento manual válido cadastrado com sucesso.")

cursor.execute("SELECT * FROM lancamento;")

print("Lançamentos cadastrados:")

for lancamento in cursor.fetchall():
    print(lancamento)
    
try:
    cursor.execute("""
        INSERT INTO lancamento (
            tipo,
            descricao,
            valor_previsto,
            data_prevista,
            categoria_id,
            status,
            origem
        )
        VALUES (?, ?, ?, ?, ?, ?, ?);
    """, (
        "OUTRO",
        "Teste tipo inválido",
        10000,
        "2026-10-06",
        1,
        "PENDENTE",
        "MANUAL"
    ))

    conexao.commit()

except sqlite3.IntegrityError as erro:
    print("Erro esperado ao testar tipo inválido:")
    print(erro)
    
try:
    cursor.execute("""
        INSERT INTO lancamento (
            tipo,
            descricao,
            valor_previsto,
            data_prevista,
            categoria_id,
            status,
            origem
        )
        VALUES (?, ?, ?, ?, ?, ?, ?);
    """, (
        "DESPESA",
        "Teste valor inválido",
        0,
        "2026-10-06",
        1,
        "PENDENTE",
        "MANUAL"
    ))

    conexao.commit()

except sqlite3.IntegrityError as erro:
    print("Erro esperado ao testar valor inválido:")
    print(erro)
    
try:
    cursor.execute("""
        INSERT INTO lancamento (
            tipo,
            descricao,
            valor_previsto,
            data_prevista,
            categoria_id,
            status,
            origem
        )
        VALUES (?, ?, ?, ?, ?, ?, ?);
    """, (
        "DESPESA",
        "Teste status inválido",
        10000,
        "2026-10-06",
        1,
        "PAGO",
        "MANUAL"
    ))

    conexao.commit()

except sqlite3.IntegrityError as erro:
    print("Erro esperado ao testar status inválido:")
    print(erro)
    
try:
    cursor.execute("""
        INSERT INTO lancamento (
            tipo,
            descricao,
            valor_previsto,
            data_prevista,
            categoria_id,
            status,
            origem
        )
        VALUES (?, ?, ?, ?, ?, ?, ?);
    """, (
        "DESPESA",
        "Teste origem inválida",
        10000,
        "2026-10-06",
        1,
        "PENDENTE",
        "OUTRA"
    ))

    conexao.commit()

except sqlite3.IntegrityError as erro:
    print("Erro esperado ao testar origem inválida:")
    print(erro)
    
try:
    cursor.execute("""
        INSERT INTO lancamento (
            tipo,
            descricao,
            valor_previsto,
            data_prevista,
            categoria_id,
            status,
            origem
        )
        VALUES (?, ?, ?, ?, ?, ?, ?);
    """, (
        "DESPESA",
        "Teste origem inválida",
        10000,
        "2026-10-06",
        "999",
        "PENDENTE",
        "MANUAL"
    ))

    conexao.commit()

except sqlite3.IntegrityError as erro:
    print("Erro esperado ao testar origem inválida:")
    print(erro)
    
try:
    cursor.execute("""
        INSERT INTO lancamento (
            tipo,
            descricao,
            valor_previsto,
            data_prevista,
            categoria_id,
            status,
            origem
        )
        VALUES (?, ?, ?, ?, ?, ?, ?);
    """, (
        "DESPESA",
        "Teste origem inválida",
        10000,
        "2026-10-06",
        None,
        "PENDENTE",
        "MANUAL"
    ))

    conexao.commit()

except sqlite3.IntegrityError as erro:
    print("Erro esperado ao testar origem inválida:")
    print(erro)
    
try:
    cursor.execute("""
        INSERT INTO lancamento (
            tipo,
            descricao,
            valor_previsto,
            data_prevista,
            categoria_id,
            status,
            origem
        )
        VALUES (?, ?, ?, ?, ?, ?, ?);
    """, (
        "DESPESA",
        "Teste fatura válida",
        10000,
        "2026-10-06",
        None,
        "PENDENTE",
        "FATURA"
    ))

    conexao.commit()

    print("Lançamento de fatura válido cadastrado com sucesso.")

except sqlite3.IntegrityError as erro:
    print("Erro inesperado ao cadastrar lançamento de fatura válido:")
    print(erro)
    
try:
    cursor.execute("""
        INSERT INTO lancamento (
            tipo,
            descricao,
            valor_previsto,
            data_prevista,
            categoria_id,
            fatura_id,
            status,
            origem
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    """, (
        "DESPESA",
        "Teste fatura sem vínculo",
        10000,
        "2026-10-10",
        None,
        None,
        "PENDENTE",
        "FATURA"
    ))

    conexao.commit()

except sqlite3.IntegrityError as erro:
    print("Erro esperado ao testar fatura sem fatura_id:")
    print(erro)
    
try:
    cursor.execute("""
        INSERT INTO lancamento (
            tipo,
            descricao,
            valor_previsto,
            data_prevista,
            categoria_id,
            fatura_id,
            status,
            origem
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    """, (
        "DESPESA",
        "Fatura Nubank Outubro",
        10000,
        "2026-10-10",
        None,
        1,
        "PENDENTE",
        "FATURA"
    ))

    conexao.commit()

    print("Lançamento de fatura válido cadastrado com sucesso.")

except sqlite3.IntegrityError as erro:
    print("Erro inesperado ao cadastrar lançamento de fatura válido:")
    print(erro)
    
try:
    cursor.execute("""
        INSERT INTO lancamento (
            tipo,
            descricao,
            valor_previsto,
            data_prevista,
            categoria_id,
            recorrencia_id,
            status,
            origem
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    """, (
        "DESPESA",
        "Teste recorrência sem vínculo",
        18300,
        "2026-11-10",
        1,
        None,
        "PENDENTE",
        "RECORRENCIA"
    ))

    conexao.commit()

except sqlite3.IntegrityError as erro:
    print("Erro esperado ao testar recorrência sem recorrencia_id:")
    print(erro)
    
try:
    cursor.execute("""
        INSERT INTO lancamento (
            tipo,
            descricao,
            valor_previsto,
            data_prevista,
            categoria_id,
            recorrencia_id,
            status,
            origem
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    """, (
        "DESPESA",
        "Internet Novembro",
        18300,
        "2026-11-10",
        1,
        1,
        "PENDENTE",
        "RECORRENCIA"
    ))

    conexao.commit()

    print("Lançamento de recorrência válido cadastrado com sucesso.")

except sqlite3.IntegrityError as erro:
    print("Erro inesperado ao cadastrar lançamento de recorrência válido:")
    print(erro)
    
try:
    cursor.execute("""
        INSERT INTO lancamento (
            tipo,
            descricao,
            valor_previsto,
            data_prevista,
            categoria_id,
            recorrencia_id,
            status,
            origem
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    """, (
        "DESPESA",
        "Teste recorrência inexistente",
        18300,
        "2026-11-10",
        1,
        999,
        "PENDENTE",
        "RECORRENCIA"
    ))

    conexao.commit()

except sqlite3.IntegrityError as erro:
    print("Erro esperado ao testar recorrencia_id inexistente:")
    print(erro)
    
try:
    cursor.execute("""
        INSERT INTO lancamento (
            tipo,
            descricao,
            valor_previsto,
            data_prevista,
            categoria_id,
            fatura_id,
            status,
            origem
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    """, (
        "DESPESA",
        "Teste fatura inexistente",
        10000,
        "2026-10-10",
        None,
        999,
        "PENDENTE",
        "FATURA"
    ))

    conexao.commit()

except sqlite3.IntegrityError as erro:
    print("Erro esperado ao testar fatura_id inexistente:")
    print(erro)
    
try:
    cursor.execute("""
        INSERT INTO lancamento (
            tipo,
            descricao,
            valor_previsto,
            data_prevista,
            categoria_id,
            fatura_id,
            status,
            origem
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    """, (
        "DESPESA",
        "Segunda tentativa da mesma fatura",
        10000,
        "2026-10-10",
        None,
        1,
        "PENDENTE",
        "FATURA"
    ))

    conexao.commit()

except sqlite3.IntegrityError as erro:
    print("Erro esperado ao testar fatura duplicada em lançamento:")
    print(erro)
    
cursor.execute("""
    INSERT INTO movimentacao (
        lancamento_id,
        valor,
        data_movimentacao,
        forma,
        observacao
    )
    VALUES (?, ?, ?, ?, ?);
""", (
    1,
    25000,
    "2026-10-05",
    "PIX",
    "Pagamento do supermercado"
))

conexao.commit()

print("Movimentação válida cadastrada com sucesso.")

cursor.execute("SELECT * FROM movimentacao;")

print("Movimentações cadastradas:")

for movimentacao in cursor.fetchall():
    print(movimentacao)
    
try:
    cursor.execute("""
        INSERT INTO movimentacao (
            lancamento_id,
            valor,
            data_movimentacao,
            forma,
            observacao
        )
        VALUES (?, ?, ?, ?, ?);
    """, (
        2,
        0,
        "2026-10-06",
        "PIX",
        "Teste valor inválido"
    ))

    conexao.commit()

except sqlite3.IntegrityError as erro:
    print("Erro esperado ao testar valor inválido:")
    print(erro)
    
try:
    cursor.execute("""
        INSERT INTO movimentacao (
            lancamento_id,
            valor,
            data_movimentacao,
            forma,
            observacao
        )
        VALUES (?, ?, ?, ?, ?);
    """, (
        2,
        10000,
        "2026-10-06",
        "CHEQUE",
        "Teste forma inválida"
    ))

    conexao.commit()

except sqlite3.IntegrityError as erro:
    print("Erro esperado ao testar forma inválida:")
    print(erro)
    
try:
    cursor.execute("""
        INSERT INTO movimentacao (
            lancamento_id,
            valor,
            data_movimentacao,
            forma,
            observacao
        )
        VALUES (?, ?, ?, ?, ?);
    """, (
        999,
        10000,
        "2026-10-06",
        "PIX",
        "Teste lançamento inexistente"
    ))

    conexao.commit()

except sqlite3.IntegrityError as erro:
    print("Erro esperado ao testar lançamento inexistente:")
    print(erro)
    
try:
    cursor.execute("""
        INSERT INTO movimentacao (
            lancamento_id,
            valor,
            data_movimentacao,
            forma,
            observacao
        )
        VALUES (?, ?, ?, ?, ?);
    """, (
        1,
        25000,
        "2026-10-07",
        "DINHEIRO",
        "Segunda movimentação do mesmo lançamento"
    ))

    conexao.commit()

except sqlite3.IntegrityError as erro:
    print("Erro esperado ao testar movimentação duplicada:")
    print(erro)
        
conexao.close()
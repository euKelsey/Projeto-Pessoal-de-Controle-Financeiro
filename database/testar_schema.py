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
    print("Erro esperado ao testar dia de referência inválido:")
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
        999,
        "2026-11",
        "2026-11-02",
        "2026-11-10",
        "ABERTA"
    ))
    
    conexao.commit()
    
except sqlite3.IntegrityError as erro:
    print("Erro esperado ao testar cartão inexistente:")
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
    print("Erro esperado ao testar status inválido:")
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
    print("Erro esperado ao testar status inválido:")
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
        "Teste categoria inexistente",
        10000,
        "2026-10-06",
        999,
        "PENDENTE",
        "MANUAL"
    ))

    conexao.commit()

except sqlite3.IntegrityError as erro:
    print("Erro esperado ao testar categoria_id inexistente:")
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
        "Teste lançamento manual sem categoria",
        10000,
        "2026-10-06",
        None,
        "PENDENTE",
        "MANUAL"
    ))

    conexao.commit()

except sqlite3.IntegrityError as erro:
    print("Erro esperado ao testar lançamento manual sem categoria:")
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
    
cursor.execute("""
    INSERT INTO compra_cartao (
        cartao_id,
        categoria_id,
        recorrencia_id,
        descricao,
        data_compra,
        valor_total,
        quantidade_parcelas,
        primeira_parcela_controlada,
        data_primeira_parcela_controlada,
        status,
        observacao
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
""", (
    1,
    1,
    None,
    "Compra supermercado",
    "2026-10-04",
    30000,
    3,
    0,
    None,
    "ATIVA",
    "Compra parcelada em 3 vezes"
))

conexao.commit()

print("Compra no cartão válida cadastrada com sucesso.")

cursor.execute("SELECT * FROM compra_cartao;")

print("Compras no cartão cadastradas:")

for compra in cursor.fetchall():
    print(compra)
    
try:
    cursor.execute("""
        INSERT INTO compra_cartao (
            cartao_id,
            categoria_id,
            recorrencia_id,
            descricao,
            data_compra,
            valor_total,
            quantidade_parcelas,
            primeira_parcela_controlada,
            data_primeira_parcela_controlada,
            status,
            observacao
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, (
        1,
        1,
        None,
        "Teste valor inválido",
        "2026-10-04",
        0,
        3,
        0,
        None,
        "ATIVA",
        None
    ))

    conexao.commit()

except sqlite3.IntegrityError as erro:
    print("Erro esperado ao testar valor_total inválido:")
    print(erro)
    
try:
    cursor.execute("""
        INSERT INTO compra_cartao (
            cartao_id,
            categoria_id,
            recorrencia_id,
            descricao,
            data_compra,
            valor_total,
            quantidade_parcelas,
            primeira_parcela_controlada,
            data_primeira_parcela_controlada,
            status,
            observacao
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, (
        1,
        1,
        None,
        "Teste quantidade inválida",
        "2026-10-04",
        30000,
        0,
        0,
        None,
        "ATIVA",
        None
    ))

    conexao.commit()

except sqlite3.IntegrityError as erro:
    print("Erro esperado ao testar quantidade_parcelas inválida:")
    print(erro)
    
try:
    cursor.execute("""
        INSERT INTO compra_cartao (
            cartao_id,
            categoria_id,
            recorrencia_id,
            descricao,
            data_compra,
            valor_total,
            quantidade_parcelas,
            primeira_parcela_controlada,
            data_primeira_parcela_controlada,
            status,
            observacao
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, (
        1,
        1,
        None,
        "Teste controle inválido",
        "2026-10-04",
        30000,
        3,
        2,
        None,
        "ATIVA",
        None
    ))

    conexao.commit()

except sqlite3.IntegrityError as erro:
    print("Erro esperado ao testar primeira_parcela_controlada inválida:")
    print(erro)
    
try:
    cursor.execute("""
        INSERT INTO compra_cartao (
            cartao_id,
            categoria_id,
            recorrencia_id,
            descricao,
            data_compra,
            valor_total,
            quantidade_parcelas,
            primeira_parcela_controlada,
            data_primeira_parcela_controlada,
            status,
            observacao
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, (
        1,
        1,
        None,
        "Teste status inválido",
        "2026-10-04",
        30000,
        3,
        0,
        None,
        "PENDENTE",
        None
    ))

    conexao.commit()

except sqlite3.IntegrityError as erro:
    print("Erro esperado ao testar status inválido:")
    print(erro)
    
try:
    cursor.execute("""
        INSERT INTO compra_cartao (
            cartao_id,
            categoria_id,
            recorrencia_id,
            descricao,
            data_compra,
            valor_total,
            quantidade_parcelas,
            primeira_parcela_controlada,
            data_primeira_parcela_controlada,
            status,
            observacao
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, (
        999,
        1,
        None,
        "Teste cartão inexistente",
        "2026-10-04",
        30000,
        3,
        0,
        None,
        "ATIVA",
        None
    ))

    conexao.commit()

except sqlite3.IntegrityError as erro:
    print("Erro esperado ao testar cartao_id inexistente:")
    print(erro)
    
try:
    cursor.execute("""
        INSERT INTO compra_cartao (
            cartao_id,
            categoria_id,
            recorrencia_id,
            descricao,
            data_compra,
            valor_total,
            quantidade_parcelas,
            primeira_parcela_controlada,
            data_primeira_parcela_controlada,
            status,
            observacao
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, (
        1,
        999,
        None,
        "Teste categoria inexistente",
        "2026-10-04",
        30000,
        3,
        0,
        None,
        "ATIVA",
        None
    ))

    conexao.commit()

except sqlite3.IntegrityError as erro:
    print("Erro esperado ao testar categoria_id inexistente:")
    print(erro)
    
try:
    cursor.execute("""
        INSERT INTO compra_cartao (
            cartao_id,
            categoria_id,
            recorrencia_id,
            descricao,
            data_compra,
            valor_total,
            quantidade_parcelas,
            primeira_parcela_controlada,
            data_primeira_parcela_controlada,
            status,
            observacao
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, (
        1,
        1,
        999,
        "Teste recorrência inexistente",
        "2026-10-04",
        30000,
        3,
        0,
        None,
        "ATIVA",
        None
    ))

    conexao.commit()

except sqlite3.IntegrityError as erro:
    print("Erro esperado ao testar recorrencia_id inexistente:")
    print(erro)
    
try:
    cursor.execute("""
        INSERT INTO compra_cartao (
            cartao_id,
            categoria_id,
            recorrencia_id,
            descricao,
            data_compra,
            valor_total,
            quantidade_parcelas,
            primeira_parcela_controlada,
            data_primeira_parcela_controlada,
            status,
            observacao
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, (
        1,
        1,
        None,
        "Teste primeira parcela sem data",
        "2026-10-04",
        30000,
        3,
        1,
        None,
        "ATIVA",
        None
    ))

    conexao.commit()

except sqlite3.IntegrityError as erro:
    print("Erro esperado ao testar primeira parcela controlada sem data:")
    print(erro)
    
cursor.execute("""
    INSERT INTO parcela_cartao (
        compra_cartao_id,
        fatura_id,
        numero_parcela,
        valor,
        data_prevista
    )
    VALUES (?, ?, ?, ?, ?);
""", (
    1,
    1,
    1,
    10000,
    "2026-10-10"
))

conexao.commit()

print("Parcela válida cadastrada com sucesso.")

cursor.execute("SELECT * FROM parcela_cartao;")

print("Parcelas cadastradas:")

for parcela in cursor.fetchall():
    print(parcela)
    
try:
    cursor.execute("""
        INSERT INTO parcela_cartao (
            compra_cartao_id,
            fatura_id,
            numero_parcela,
            valor,
            data_prevista
        )
        VALUES (?, ?, ?, ?, ?);
    """, (
        1,
        1,
        0,
        10000,
        "2026-10-10"
    ))

    conexao.commit()

except sqlite3.IntegrityError as erro:
    print("Erro esperado ao testar numero_parcela inválido:")
    print(erro)
    
try:
    cursor.execute("""
        INSERT INTO parcela_cartao (
            compra_cartao_id,
            fatura_id,
            numero_parcela,
            valor,
            data_prevista
        )
        VALUES (?, ?, ?, ?, ?);
    """, (
        1,
        1,
        2,
        0,
        "2026-11-10"
    ))

    conexao.commit()

except sqlite3.IntegrityError as erro:
    print("Erro esperado ao testar valor inválido:")
    print(erro)
    
try:
    cursor.execute("""
        INSERT INTO parcela_cartao (
            compra_cartao_id,
            fatura_id,
            numero_parcela,
            valor,
            data_prevista
        )
        VALUES (?, ?, ?, ?, ?);
    """, (
        999,
        1,
        2,
        10000,
        "2026-11-10"
    ))

    conexao.commit()

except sqlite3.IntegrityError as erro:
    print("Erro esperado ao testar compra_cartao_id inexistente:")
    print(erro)
    
try:
    cursor.execute("""
        INSERT INTO parcela_cartao (
            compra_cartao_id,
            fatura_id,
            numero_parcela,
            valor,
            data_prevista
        )
        VALUES (?, ?, ?, ?, ?);
    """, (
        1,
        999,
        2,
        10000,
        "2026-11-10"
    ))

    conexao.commit()

except sqlite3.IntegrityError as erro:
    print("Erro esperado ao testar fatura_id inexistente:")
    print(erro)
    
try:
    cursor.execute("""
        INSERT INTO parcela_cartao (
            compra_cartao_id,
            fatura_id,
            numero_parcela,
            valor,
            data_prevista
        )
        VALUES (?, ?, ?, ?, ?);
    """, (
        1,
        1,
        1,
        10000,
        "2026-10-10"
    ))

    conexao.commit()

except sqlite3.IntegrityError as erro:
    print("Erro esperado ao testar parcela duplicada:")
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
    "2026-12",
    "2026-12-02",
    "2026-12-10",
    "ABERTA"
))

conexao.commit()

fatura_teste_id = cursor.lastrowid

print("Fatura criada para teste:", fatura_teste_id)

cursor.execute("""
    INSERT INTO parcela_cartao (
        compra_cartao_id,
        fatura_id,
        numero_parcela,
        valor,
        data_prevista
    )
    VALUES (?, ?, ?, ?, ?);
""", (
    1,
    fatura_teste_id,
    2,
    10000,
    "2026-12-10"
))

conexao.commit()

parcela_teste_id = cursor.lastrowid

print("Parcela criada para teste:", parcela_teste_id)

cursor.execute("""
    SELECT id, fatura_id
    FROM parcela_cartao
    WHERE id = ?;
""", (parcela_teste_id,))

print("Parcela antes de excluir a fatura:")
print(cursor.fetchone())

cursor.execute("""
    DELETE FROM fatura
    WHERE id = ?;
""", (fatura_teste_id,))

conexao.commit()

cursor.execute("""
    SELECT id, fatura_id
    FROM parcela_cartao
    WHERE id = ?;
""", (parcela_teste_id,))

print("Parcela depois de excluir a fatura:")
print(cursor.fetchone())

cursor.execute("""
    INSERT INTO meta_reserva (
        tipo,
        valor,
        percentual,
        data_inicio,
        data_fim,
        status,
        observacao
    )
    VALUES (?, ?, ?, ?, ?, ?, ?);
""", (
    "VALOR_FIXO",
    50000,
    None,
    "2026-10-01",
    None,
    "ATIVA",
    "Guardar R$ 500 por mês"
))

conexao.commit()

print("Meta de valor fixo cadastrada com sucesso.")

cursor.execute("""
    INSERT INTO meta_reserva (
        tipo,
        valor,
        percentual,
        data_inicio,
        data_fim,
        status,
        observacao
    )
    VALUES (?, ?, ?, ?, ?, ?, ?);
""", (
    "PERCENTUAL",
    None,
    2000,
    "2026-10-01",
    None,
    "ATIVA",
    "Guardar 20% da receita"
))

conexao.commit()

print("Meta percentual cadastrada com sucesso.")

cursor.execute("SELECT * FROM meta_reserva;")

print("Metas de reserva cadastradas:")

for meta in cursor.fetchall():
    print(meta)
    
try:
    cursor.execute("""
        INSERT INTO meta_reserva (
            tipo,
            valor,
            percentual,
            data_inicio,
            data_fim,
            status,
            observacao
        )
        VALUES (?, ?, ?, ?, ?, ?, ?);
    """, (
        "OUTRO",
        50000,
        None,
        "2026-10-01",
        None,
        "ATIVA",
        "Teste tipo inválido"
    ))

    conexao.commit()

except sqlite3.IntegrityError as erro:
    print("Erro esperado ao testar tipo inválido:")
    print(erro)
    
try:
    cursor.execute("""
        INSERT INTO meta_reserva (
            tipo,
            valor,
            percentual,
            data_inicio,
            data_fim,
            status,
            observacao
        )
        VALUES (?, ?, ?, ?, ?, ?, ?);
    """, (
        "VALOR_FIXO",
        None,
        None,
        "2026-10-01",
        None,
        "ATIVA",
        "Teste valor fixo sem valor"
    ))

    conexao.commit()

except sqlite3.IntegrityError as erro:
    print("Erro esperado ao testar VALOR_FIXO sem valor:")
    print(erro)
    
try:
    cursor.execute("""
        INSERT INTO meta_reserva (
            tipo,
            valor,
            percentual,
            data_inicio,
            data_fim,
            status,
            observacao
        )
        VALUES (?, ?, ?, ?, ?, ?, ?);
    """, (
        "VALOR_FIXO",
        50000,
        2000,
        "2026-10-01",
        None,
        "ATIVA",
        "Teste valor fixo com percentual"
    ))

    conexao.commit()

except sqlite3.IntegrityError as erro:
    print("Erro esperado ao testar VALOR_FIXO com percentual:")
    print(erro)
    
try:
    cursor.execute("""
        INSERT INTO meta_reserva (
            tipo,
            valor,
            percentual,
            data_inicio,
            data_fim,
            status,
            observacao
        )
        VALUES (?, ?, ?, ?, ?, ?, ?);
    """, (
        "PERCENTUAL",
        None,
        None,
        "2026-10-01",
        None,
        "ATIVA",
        "Teste percentual sem percentual"
    ))

    conexao.commit()

except sqlite3.IntegrityError as erro:
    print("Erro esperado ao testar PERCENTUAL sem percentual:")
    print(erro)
    
try:
    cursor.execute("""
        INSERT INTO meta_reserva (
            tipo,
            valor,
            percentual,
            data_inicio,
            data_fim,
            status,
            observacao
        )
        VALUES (?, ?, ?, ?, ?, ?, ?);
    """, (
        "PERCENTUAL",
        None,
        12000,
        "2026-10-01",
        None,
        "ATIVA",
        "Teste percentual acima de 100%"
    ))

    conexao.commit()

except sqlite3.IntegrityError as erro:
    print("Erro esperado ao testar percentual acima de 100%:")
    print(erro)
    
try:
    cursor.execute("""
        INSERT INTO meta_reserva (
            tipo,
            valor,
            percentual,
            data_inicio,
            data_fim,
            status,
            observacao
        )
        VALUES (?, ?, ?, ?, ?, ?, ?);
    """, (
        "VALOR_FIXO",
        50000,
        None,
        "2026-10-01",
        "2026-09-01",
        "ATIVA",
        "Teste data final anterior"
    ))

    conexao.commit()

except sqlite3.IntegrityError as erro:
    print("Erro esperado ao testar data_fim anterior à data_inicio:")
    print(erro)
    
try:
    cursor.execute("""
        INSERT INTO meta_reserva (
            tipo,
            valor,
            percentual,
            data_inicio,
            data_fim,
            status,
            observacao
        )
        VALUES (?, ?, ?, ?, ?, ?, ?);
    """, (
        "VALOR_FIXO",
        50000,
        None,
        "2026-10-01",
        None,
        "PAUSADA",
        "Teste status inválido"
    ))

    conexao.commit()

except sqlite3.IntegrityError as erro:
    print("Erro esperado ao testar status inválido:")
    print(erro)
    
cursor.execute("""
    INSERT INTO reserva_movimentacao (
        valor,
        data_movimentacao,
        observacao
    )
    VALUES (?, ?, ?);
""", (
    45000,
    "2026-10-04",
    "Valor reservado no mês de outubro"
))

conexao.commit()

print("Reserva realizada cadastrada com sucesso.")

cursor.execute("SELECT * FROM reserva_movimentacao;")

print("Movimentações de reserva cadastradas:")

for reserva in cursor.fetchall():
    print(reserva)
    
try:
    cursor.execute("""
        INSERT INTO reserva_movimentacao (
            valor,
            data_movimentacao,
            observacao
        )
        VALUES (?, ?, ?);
    """, (
        0,
        "2026-10-04",
        "Teste valor zero"
    ))

    conexao.commit()

except sqlite3.IntegrityError as erro:
    print("Erro esperado ao testar valor zero:")
    print(erro)
    
try:
    cursor.execute("""
        INSERT INTO reserva_movimentacao (
            valor,
            data_movimentacao,
            observacao
        )
        VALUES (?, ?, ?);
    """, (
        -10000,
        "2026-10-04",
        "Teste valor negativo"
    ))

    conexao.commit()

except sqlite3.IntegrityError as erro:
    print("Erro esperado ao testar valor negativo:")
    print(erro)
    
cursor.execute("""
    INSERT INTO configuracao (
        chave,
        valor
    )
    VALUES (?, ?);
""", (
    "moeda",
    "BRL"
))

conexao.commit()

print("Configuração válida cadastrada com sucesso.")

cursor.execute("SELECT * FROM configuracao;")

print("Configurações cadastradas:")

for configuracao in cursor.fetchall():
    print(configuracao)
    
try:
    cursor.execute("""
        INSERT INTO configuracao (
            chave,
            valor
        )
        VALUES (?, ?);
    """, (
        "moeda",
        "USD"
    ))

    conexao.commit()

except sqlite3.IntegrityError as erro:
    print("Erro esperado ao testar chave duplicada:")
    print(erro)
    
try:
    cursor.execute("""
        INSERT INTO configuracao (
            chave,
            valor
        )
        VALUES (?, ?);
    """, (
        None,
        "teste"
    ))

    conexao.commit()

except sqlite3.IntegrityError as erro:
    print("Erro esperado ao testar chave nula:")
    print(erro)
    
try:
    cursor.execute("""
        INSERT INTO configuracao (
            chave,
            valor
        )
        VALUES (?, ?);
    """, (
        "tema",
        None
    ))

    conexao.commit()

except sqlite3.IntegrityError as erro:
    print("Erro esperado ao testar valor nulo:")
    print(erro)
        

# Testes adicionais após a revisão geral do schema.

print("\nTestes adicionais de integridade:")

# Recorrência destinada a compra no cartão: caso válido.
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
            cartao_id,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, (
        "DESPESA",
        "Streaming no cartão",
        5000,
        1,
        "MENSAL",
        "2026-10-01",
        15,
        "COMPRA_CARTAO",
        1,
        "ATIVA"
    ))

    conexao.commit()
    print("Recorrência de compra no cartão válida cadastrada com sucesso.")

except sqlite3.IntegrityError as erro:
    print("Erro inesperado ao cadastrar recorrência de compra no cartão válida:")
    print(erro)

# COMPRA_CARTAO precisa ter cartao_id.
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
            cartao_id,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, (
        "DESPESA",
        "Teste compra no cartão sem cartão",
        5000,
        1,
        "MENSAL",
        "2026-10-01",
        15,
        "COMPRA_CARTAO",
        None,
        "ATIVA"
    ))

    conexao.commit()

except sqlite3.IntegrityError as erro:
    print("Erro esperado ao testar COMPRA_CARTAO sem cartao_id:")
    print(erro)

# Recorrência que gera compra no cartão deve ser uma despesa.
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
            cartao_id,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, (
        "RECEITA",
        "Teste receita no cartão",
        5000,
        1,
        "MENSAL",
        "2026-10-01",
        15,
        "COMPRA_CARTAO",
        1,
        "ATIVA"
    ))

    conexao.commit()

except sqlite3.IntegrityError as erro:
    print("Erro esperado ao testar COMPRA_CARTAO com tipo RECEITA:")
    print(erro)

# Recorrência de lançamento direto não deve ficar vinculada a um cartão.
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
            cartao_id,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, (
        "DESPESA",
        "Teste lançamento direto com cartão",
        5000,
        1,
        "MENSAL",
        "2026-10-01",
        15,
        "LANCAMENTO",
        1,
        "ATIVA"
    ))

    conexao.commit()

except sqlite3.IntegrityError as erro:
    print("Erro esperado ao testar LANCAMENTO com cartao_id:")
    print(erro)

# Valida a FK corrigida recorrencia.cartao_id -> cartao.id.
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
            cartao_id,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, (
        "DESPESA",
        "Teste cartão inexistente na recorrência",
        5000,
        1,
        "MENSAL",
        "2026-10-01",
        15,
        "COMPRA_CARTAO",
        999,
        "ATIVA"
    ))

    conexao.commit()

except sqlite3.IntegrityError as erro:
    print("Erro esperado ao testar cartao_id inexistente na recorrência:")
    print(erro)

# Cria uma fatura exclusiva para testar combinações inválidas de origem.
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
    "2027-01",
    "2027-01-02",
    "2027-01-10",
    "ABERTA"
))

conexao.commit()
fatura_origem_teste_id = cursor.lastrowid

# MANUAL não pode carregar recorrencia_id.
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
        "Teste manual com recorrência",
        10000,
        "2027-01-05",
        1,
        1,
        "PENDENTE",
        "MANUAL"
    ))

    conexao.commit()

except sqlite3.IntegrityError as erro:
    print("Erro esperado ao testar MANUAL com recorrencia_id:")
    print(erro)

# RECORRENCIA não pode carregar fatura_id.
try:
    cursor.execute("""
        INSERT INTO lancamento (
            tipo,
            descricao,
            valor_previsto,
            data_prevista,
            categoria_id,
            recorrencia_id,
            fatura_id,
            status,
            origem
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, (
        "DESPESA",
        "Teste recorrência com fatura",
        10000,
        "2027-01-05",
        1,
        1,
        fatura_origem_teste_id,
        "PENDENTE",
        "RECORRENCIA"
    ))

    conexao.commit()

except sqlite3.IntegrityError as erro:
    print("Erro esperado ao testar RECORRENCIA com fatura_id:")
    print(erro)

# FATURA não pode carregar recorrencia_id.
try:
    cursor.execute("""
        INSERT INTO lancamento (
            tipo,
            descricao,
            valor_previsto,
            data_prevista,
            categoria_id,
            recorrencia_id,
            fatura_id,
            status,
            origem
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, (
        "DESPESA",
        "Teste fatura com recorrência",
        10000,
        "2027-01-10",
        None,
        1,
        fatura_origem_teste_id,
        "PENDENTE",
        "FATURA"
    ))

    conexao.commit()

except sqlite3.IntegrityError as erro:
    print("Erro esperado ao testar FATURA com recorrencia_id:")
    print(erro)

# Um lançamento de fatura deve ser sempre uma despesa.
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
        "RECEITA",
        "Teste fatura como receita",
        10000,
        "2027-01-10",
        None,
        fatura_origem_teste_id,
        "PENDENTE",
        "FATURA"
    ))

    conexao.commit()

except sqlite3.IntegrityError as erro:
    print("Erro esperado ao testar FATURA com tipo RECEITA:")
    print(erro)

# Remove a fatura criada apenas para os testes de origem.
cursor.execute("""
    DELETE FROM fatura
    WHERE id = ?;
""", (fatura_origem_teste_id,))
conexao.commit()

# A recorrência 1 possui um lançamento associado e não deve ser apagada em cascata.
try:
    cursor.execute("""
        DELETE FROM recorrencia
        WHERE id = ?;
    """, (1,))

    conexao.commit()

except sqlite3.IntegrityError as erro:
    print("Erro esperado ao testar ON DELETE RESTRICT de recorrencia -> lancamento:")
    print(erro)

# Verificação final das chaves estrangeiras.
cursor.execute("PRAGMA foreign_key_check;")
erros_fk = cursor.fetchall()

if erros_fk:
    print("Foram encontrados problemas de chave estrangeira:")
    for erro_fk in erros_fk:
        print(erro_fk)
else:
    print("PRAGMA foreign_key_check: nenhuma inconsistência encontrada.")


conexao.close()

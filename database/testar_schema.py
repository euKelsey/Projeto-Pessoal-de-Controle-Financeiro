import sqlite3
from pathlib import Path

PASTA_DATABASE = Path(__file__).parent

CAMINHO_SCHEMA = PASTA_DATABASE / "schema.sql"
CAMINHO_BANCO = PASTA_DATABASE / "controle_financeiro.db"

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

cursor = conexao.cursor()

cursor.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type = 'table';
""")

tabelas = cursor.fetchall()

print("Tabelas encontradas:")
print(tabelas)

#cursor.execute("""
#    INSERT INTO categoria (nome, tipo, descricao)
#    VALUES (?, ?, ?);
#""", ("Alimentação", "DESPESA", "Gastos com alimentação"))

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

for categoria in categorias:
    print(categoria)

conexao.close()
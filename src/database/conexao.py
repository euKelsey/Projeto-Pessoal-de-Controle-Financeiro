import sqlite3
from pathlib import Path

PASTA_PROJETO = Path(__file__).resolve().parents[2]

CAMINHO_BANCO = PASTA_PROJETO / "database" / "controle_financeiro.db"

def conectar():
    conexao = sqlite3.connect(CAMINHO_BANCO)
    conexao.execute("PRAGMA foreign_keys = ON;")
    
    return conexao 

def inicializar_banco():
    conexao = conectar()
    
    caminho_schema = PASTA_PROJETO / "database" / "schema.sql"
    
    with open(caminho_schema, "r", encoding="utf-8") as arquivo:
        schema = arquivo.read()
        
        conexao.executescript(schema)
        conexao.commit()
        conexao.close()
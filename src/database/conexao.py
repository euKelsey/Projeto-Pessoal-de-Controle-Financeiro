
import os
import sys
import sqlite3

from pathlib import Path


# ============================================
# CAMINHO DOS ARQUIVOS DO PROGRAMA
# ============================================

if getattr(sys, "frozen", False):

    # Quando estiver rodando como executável
    PASTA_RECURSOS = Path(sys._MEIPASS)

else:

    # Quando estiver rodando pelo Python
    PASTA_RECURSOS = Path(__file__).resolve().parents[2]


# ============================================
# PASTA PERMANENTE DO BANCO DE DADOS
# ============================================

pasta_local = os.getenv("LOCALAPPDATA")

if pasta_local:

    PASTA_DADOS = (
        Path(pasta_local) / "ControleFinanceiro"
    )

else:

    PASTA_DADOS = (
        Path.home()
        / "AppData"
        / "Local"
        / "ControleFinanceiro"
    )


# Criar a pasta caso ainda não exista
PASTA_DADOS.mkdir(
    parents=True,
    exist_ok=True
)


# Caminho definitivo do banco
CAMINHO_BANCO = (
    PASTA_DADOS / "controle_financeiro.db"
)


# Caminho do arquivo de estrutura
CAMINHO_SCHEMA = (
    PASTA_RECURSOS / "database" / "schema.sql"
)


# ============================================
# CONEXÃO COM O SQLITE
# ============================================

def conectar():

    conexao = sqlite3.connect(
        CAMINHO_BANCO
    )

    conexao.execute(
        "PRAGMA foreign_keys = ON;"
    )

    return conexao


# ============================================
# INICIALIZAÇÃO DO BANCO
# ============================================

def inicializar_banco():

    with open(
        CAMINHO_SCHEMA,
        "r",
        encoding="utf-8"
    ) as arquivo:

        schema = arquivo.read()

    conexao = conectar()

    try:

        conexao.executescript(schema)

        conexao.commit()

    finally:

        conexao.close()

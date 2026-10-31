
import sys
import sqlite3
import tempfile
from pathlib import Path
from unittest.mock import patch

sys.path.insert(
    0,
    str(Path(__file__).resolve().parent / "src")
)

from models.compra_cartao import CompraCartao
from repositories.compra_cartao_repository import (
    inserir_compra_com_parcela
)

with tempfile.TemporaryDirectory() as pasta:
    banco_teste = Path(pasta) / "teste.db"

    conexao = sqlite3.connect(banco_teste)
    conexao.execute("PRAGMA foreign_keys = ON")

    schema = (
        Path(__file__).resolve().parent
        / "database"
        / "schema.sql"
    ).read_text(encoding="utf-8")

    conexao.executescript(schema)

    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO categoria (nome, tipo, status)
        VALUES ('Teste', 'DESPESA', 'ATIVA');
    """)
    categoria_id = cursor.lastrowid


    cursor.execute("""
        INSERT INTO cartao (
            nome,
            instituicao,
            limite_total,
            dia_fechamento,
            dia_vencimento,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?);
    """, (
        "Cartao Teste",
        "Banco Teste",
        100000,
        5,
        12,
        "ATIVO"
    ))

    cartao_id = cursor.lastrowid


    cursor.execute("""
        INSERT INTO fatura (
            cartao_id, mes_referencia,
            data_fechamento, data_vencimento, status
        )
        VALUES (?, '2026-11', '2026-11-05',
                '2026-11-12', 'FECHADA');
    """, (cartao_id,))

    conexao.commit()
    conexao.close()

    def conectar_teste():
        conexao = sqlite3.connect(banco_teste)
        conexao.execute("PRAGMA foreign_keys = ON")
        return conexao

    compra = CompraCartao(
        id=None,
        cartao_id=cartao_id,
        categoria_id=categoria_id,
        descricao="Compra bloqueada",
        data_compra="2026-10-31",
        valor_total=25990,
        quantidade_parcelas=1
    )

    with patch(
        "repositories.compra_cartao_repository.conectar",
        conectar_teste
    ):
        try:
            inserir_compra_com_parcela(
                compra,
                "2026-11",
                "2026-11-05",
                "2026-11-12"
            )
            print("FALHOU: compra foi aceita")

        except ValueError as erro:
            print("Bloqueio funcionando:", erro)

    conexao = conectar_teste()

    total_compras = conexao.execute(
        "SELECT COUNT(*) FROM compra_cartao"
    ).fetchone()[0]

    total_parcelas = conexao.execute(
        "SELECT COUNT(*) FROM parcela_cartao"
    ).fetchone()[0]

    conexao.close()

    print("Compras gravadas:", total_compras)
    print("Parcelas gravadas:", total_parcelas)

    assert total_compras == 0
    assert total_parcelas == 0

    print("Teste de rollback OK")

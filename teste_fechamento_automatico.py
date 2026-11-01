
import sys
import sqlite3
import tempfile
from pathlib import Path
from contextlib import closing
from unittest.mock import patch

RAIZ = Path(__file__).resolve().parent
sys.path.insert(0, str(RAIZ / "src"))

from services.fatura_service import atualizar_faturas_automaticamente


def executar_teste():
    with tempfile.TemporaryDirectory() as pasta:
        banco_teste = Path(pasta) / "fechamento.db"

        def conectar_teste():
            conexao = sqlite3.connect(banco_teste)
            conexao.execute("PRAGMA foreign_keys = ON")
            return conexao

        # Preparar banco temporário.
        with closing(conectar_teste()) as conexao:
            schema = (RAIZ / "database" / "schema.sql").read_text(
                encoding="utf-8"
            )
            conexao.executescript(schema)

            cursor = conexao.cursor()

            cursor.execute("""
                INSERT INTO cartao (
                    nome, instituicao, limite_total,
                    dia_fechamento, dia_vencimento, status
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

            faturas = [
                ("2026-10", "2026-10-05", "2026-10-12"),
                ("2026-11", "2026-11-05", "2026-11-12"),
                ("2026-12", "2026-12-05", "2026-12-12")
            ]

            for mes, fechamento, vencimento in faturas:
                cursor.execute("""
                    INSERT INTO fatura (
                        cartao_id, mes_referencia,
                        data_fechamento, data_vencimento, status
                    )
                    VALUES (?, ?, ?, ?, 'ABERTA');
                """, (
                    cartao_id,
                    mes,
                    fechamento,
                    vencimento
                ))

            conexao.commit()

        # Simular a data de 05/11/2026.
        with patch(
            "repositories.fatura_repository.conectar",
            conectar_teste
        ):
            quantidade = atualizar_faturas_automaticamente(
                "2026-11-05"
            )

            print("Faturas fechadas:", quantidade)

            assert quantidade == 2

            # Executar novamente não deve fechar nada.
            segunda_execucao = atualizar_faturas_automaticamente(
                "2026-11-05"
            )

            assert segunda_execucao == 0

        with closing(conectar_teste()) as conexao:
            registros = conexao.execute("""
                SELECT mes_referencia, status
                FROM fatura
                ORDER BY mes_referencia;
            """).fetchall()

        for mes, status in registros:
            print(mes, status)

        assert registros == [
            ("2026-10", "FECHADA"),
            ("2026-11", "FECHADA"),
            ("2026-12", "ABERTA")
        ]

        print("Teste de fechamento automatico OK")


if __name__ == "__main__":
    executar_teste()

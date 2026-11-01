
import sys
import sqlite3
import tempfile
from pathlib import Path
from contextlib import closing
from unittest.mock import patch

RAIZ = Path(__file__).resolve().parent
sys.path.insert(0, str(RAIZ / "src"))

from repositories.fatura_repository import gerar_lancamento_fatura


def executar_teste():
    with tempfile.TemporaryDirectory() as pasta:
        banco_teste = Path(pasta) / "lancamento_fatura.db"

        def conectar_teste():
            conexao = sqlite3.connect(banco_teste)
            conexao.execute("PRAGMA foreign_keys = ON")
            return conexao

        # 1. Criar banco e registros de demonstração.
        with closing(conectar_teste()) as conexao:
            schema = (RAIZ / "database" / "schema.sql").read_text(
                encoding="utf-8"
            )
            conexao.executescript(schema)

            cursor = conexao.cursor()

            cursor.execute("""
                INSERT INTO categoria (nome, tipo, status)
                VALUES ('Teste', 'DESPESA', 'ATIVA');
            """)
            categoria_id = cursor.lastrowid

            cursor.execute("""
                INSERT INTO cartao (
                    nome, instituicao, limite_total,
                    dia_fechamento, dia_vencimento, status
                )
                VALUES (?, ?, ?, ?, ?, ?);
            """, (
                "Cartao Teste", "Banco Teste",
                100000, 5, 12, "ATIVO"
            ))
            cartao_id = cursor.lastrowid

            faturas = [
                ("2026-10", "FECHADA"),
                ("2026-11", "ABERTA"),
                ("2026-12", "FECHADA")
            ]

            ids_faturas = []

            for mes, status in faturas:
                ano, numero_mes = mes.split("-")
                fechamento = f"{mes}-05"
                vencimento = f"{mes}-12"

                cursor.execute("""
                    INSERT INTO fatura (
                        cartao_id, mes_referencia,
                        data_fechamento, data_vencimento, status
                    )
                    VALUES (?, ?, ?, ?, ?);
                """, (
                    cartao_id, mes, fechamento,
                    vencimento, status
                ))
                ids_faturas.append(cursor.lastrowid)

            cursor.execute("""
                INSERT INTO compra_cartao (
                    cartao_id, categoria_id, descricao,
                    data_compra, valor_total,
                    quantidade_parcelas, status
                )
                VALUES (?, ?, ?, ?, ?, 1, 'ATIVA');
            """, (
                cartao_id, categoria_id,
                "Compra teste", "2026-10-01", 25990
            ))
            compra_id = cursor.lastrowid

            cursor.execute("""
                INSERT INTO parcela_cartao (
                    compra_cartao_id, fatura_id,
                    numero_parcela, valor, data_prevista
                )
                VALUES (?, ?, 1, 25990, '2026-10-12');
            """, (
                compra_id, ids_faturas[0]
            ))

            conexao.commit()

        with patch(
            "repositories.fatura_repository.conectar",
            conectar_teste
        ):
            # Teste 1 - Fatura fechada com compra.
            lancamento_id = gerar_lancamento_fatura(ids_faturas[0])

            assert lancamento_id is not None
            print("Teste 1: lancamento criado OK")

            # Teste 2 - A mesma fatura não pode duplicar.
            segundo_id = gerar_lancamento_fatura(ids_faturas[0])

            assert segundo_id == lancamento_id
            print("Teste 2: sem duplicidade OK")

            # Teste 3 - Fatura aberta deve ser bloqueada.
            try:
                gerar_lancamento_fatura(ids_faturas[1])
                raise AssertionError("Fatura aberta foi aceita.")
            except ValueError as erro:
                assert "fechada" in str(erro).lower()
                print("Teste 3: fatura aberta bloqueada OK")

            # Teste 4 - Fatura sem compras.
            resultado = gerar_lancamento_fatura(ids_faturas[2])

            assert resultado is None
            print("Teste 4: fatura sem compras OK")

        # Conferir o resultado efetivamente gravado.
        with closing(conectar_teste()) as conexao:
            registros = conexao.execute("""
                SELECT fatura_id, valor_previsto,
                       status, origem, data_prevista
                FROM lancamento
                WHERE origem = 'FATURA';
            """).fetchall()

            assert registros == [
                (
                    ids_faturas[0],
                    25990,
                    "PENDENTE",
                    "FATURA",
                    "2026-10-12"
                )
            ]

        print("Todos os testes de lancamento passaram!")


if __name__ == "__main__":
    executar_teste()

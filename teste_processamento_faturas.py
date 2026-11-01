
import sys
import sqlite3
import tempfile
from pathlib import Path
from contextlib import closing
from unittest.mock import patch

RAIZ = Path(__file__).resolve().parent
sys.path.insert(0, str(RAIZ / "src"))

from repositories.fatura_repository import processar_faturas_automaticamente
from services.fatura_service import atualizar_faturas_automaticamente


def executar_testes():
    with tempfile.TemporaryDirectory() as pasta:
        banco_teste = Path(pasta) / "processamento.db"

        def conectar_teste():
            conexao = sqlite3.connect(banco_teste)
            conexao.execute("PRAGMA foreign_keys = ON")
            return conexao

        # Preparar o banco temporário
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
            """, ("Cartao Teste", "Banco Teste", 100000, 5, 12, "ATIVO"))
            cartao_id = cursor.lastrowid

            for mes, fechamento, vencimento in [
                ("2026-10", "2026-10-05", "2026-10-12"),
                ("2026-11", "2026-11-05", "2026-11-12"),
                ("2026-12", "2026-12-05", "2026-12-12")
            ]:
                cursor.execute("""
                    INSERT INTO fatura (
                        cartao_id, mes_referencia,
                        data_fechamento, data_vencimento, status
                    )
                    VALUES (?, ?, ?, ?, 'ABERTA');
                """, (cartao_id, mes, fechamento, vencimento))

            # Compra ativa de R$ 259,90
            cursor.execute("""
                INSERT INTO compra_cartao (
                    cartao_id, categoria_id, descricao,
                    data_compra, valor_total,
                    quantidade_parcelas, status
                )
                VALUES (?, ?, ?, ?, ?, 1, 'ATIVA');
            """, (
                cartao_id, categoria_id,
                "Compra ativa", "2026-10-01", 25990
            ))
            compra_ativa = cursor.lastrowid

            cursor.execute("""
                INSERT INTO parcela_cartao (
                    compra_cartao_id, fatura_id,
                    numero_parcela, valor, data_prevista
                )
                VALUES (?, 1, 1, 25990, '2026-10-12');
            """, (compra_ativa,))

            # Compra cancelada de R$ 100,00
            cursor.execute("""
                INSERT INTO compra_cartao (
                    cartao_id, categoria_id, descricao,
                    data_compra, valor_total,
                    quantidade_parcelas, status
                )
                VALUES (?, ?, ?, ?, ?, 1, 'CANCELADA');
            """, (
                cartao_id, categoria_id,
                "Compra cancelada", "2026-10-02", 10000
            ))
            compra_cancelada = cursor.lastrowid

            cursor.execute("""
                INSERT INTO parcela_cartao (
                    compra_cartao_id, fatura_id,
                    numero_parcela, valor, data_prevista
                )
                VALUES (?, 1, 1, 10000, '2026-10-12');
            """, (compra_cancelada,))

            conexao.commit()

        # TESTES 1 a 4
        with patch(
            "repositories.fatura_repository.conectar",
            conectar_teste
        ):
            fechadas, lancamentos = processar_faturas_automaticamente(
                "2026-11-05"
            )

            assert fechadas == 2
            assert lancamentos == 1
            print("Teste 1: fechamento automatico OK")
            print("Teste 2: lancamento criado OK")

            fechadas2, lancamentos2 = processar_faturas_automaticamente(
                "2026-11-05"
            )

            assert (fechadas2, lancamentos2) == (0, 0)
            print("Teste 3: sem duplicidade OK")

        with closing(conectar_teste()) as conexao:
            registros = conexao.execute("""
                SELECT fatura_id, valor_previsto, origem, status
                FROM lancamento;
            """).fetchall()

            assert registros == [
                (1, 25990, "FATURA", "PENDENTE")
            ]

            print("Teste 4: compra cancelada excluida OK")

            status_dezembro = conexao.execute("""
                SELECT status
                FROM fatura
                WHERE mes_referencia = '2026-12';
            """).fetchone()[0]

            assert status_dezembro == "ABERTA"

        # TESTE 5 - Simular falha no INSERT do lançamento.
        # Criamos uma nova fatura vencida com compra.
        with closing(conectar_teste()) as conexao:
            cursor = conexao.cursor()

            cursor.execute("""
                INSERT INTO fatura (
                    cartao_id, mes_referencia,
                    data_fechamento, data_vencimento, status
                )
                VALUES (?, '2026-09', '2026-09-05',
                        '2026-09-12', 'ABERTA');
            """, (cartao_id,))

            fatura_falha_id = cursor.lastrowid

            cursor.execute("""
                INSERT INTO compra_cartao (
                    cartao_id, categoria_id, descricao,
                    data_compra, valor_total,
                    quantidade_parcelas, status
                )
                VALUES (?, ?, 'Compra rollback',
                        '2026-09-01', 5000, 1, 'ATIVA');
            """, (cartao_id, categoria_id))

            compra_falha_id = cursor.lastrowid

            cursor.execute("""
                INSERT INTO parcela_cartao (
                    compra_cartao_id, fatura_id,
                    numero_parcela, valor, data_prevista
                )
                VALUES (?, ?, 1, 5000, '2026-09-12');
            """, (compra_falha_id, fatura_falha_id))

            # Trigger temporário que força erro no INSERT.
            cursor.execute("""
                CREATE TRIGGER bloquear_lancamento_teste
                BEFORE INSERT ON lancamento
                BEGIN
                    SELECT RAISE(ABORT, 'Falha simulada');
                END;
            """)

            conexao.commit()

        with patch(
            "repositories.fatura_repository.conectar",
            conectar_teste
        ):
            try:
                processar_faturas_automaticamente("2026-11-05")
                raise AssertionError("Falha simulada nao foi detectada.")
            except sqlite3.IntegrityError:
                print("Teste 5: rollback acionado OK")

        with closing(conectar_teste()) as conexao:
            status = conexao.execute("""
                SELECT status FROM fatura WHERE id = ?;
            """, (fatura_falha_id,)).fetchone()[0]

            assert status == "ABERTA"

            total = conexao.execute("""
                SELECT COUNT(*) FROM lancamento
                WHERE fatura_id = ?;
            """, (fatura_falha_id,)).fetchone()[0]

            assert total == 0
            
        # TESTE 6 - Integração Service + Repository
        with closing(conectar_teste()) as conexao:
            conexao.execute("""
                DROP TRIGGER bloquear_lancamento_teste;
            """)
            conexao.commit()

        with patch(
            "repositories.fatura_repository.conectar",
            conectar_teste
        ):
            quantidade = atualizar_faturas_automaticamente(
                "2026-11-05"
            )

            assert quantidade == 1

        with closing(conectar_teste()) as conexao:
            registro = conexao.execute("""
                SELECT
                    f.status,
                    l.valor_previsto,
                    l.status,
                    l.origem
                FROM fatura AS f
                INNER JOIN lancamento AS l
                    ON l.fatura_id = f.id
                WHERE f.id = ?;
            """, (fatura_falha_id,)).fetchone()

            assert registro == (
                "FECHADA",
                5000,
                "PENDENTE",
                "FATURA"
            )

        print("Teste 6: integracao Service + Repository OK")

        print("Todos os testes de processamento passaram!")


if __name__ == "__main__":
    executar_testes()

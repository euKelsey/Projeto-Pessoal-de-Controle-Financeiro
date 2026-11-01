
import sys
import sqlite3
import tempfile
from pathlib import Path
from contextlib import closing
from datetime import date, timedelta
from unittest.mock import patch

RAIZ = Path(__file__).resolve().parent
sys.path.insert(0, str(RAIZ / "src"))

from models.compra_cartao import CompraCartao
from repositories.compra_cartao_repository import inserir_compra_com_parcela


def executar_teste():
    with tempfile.TemporaryDirectory() as pasta:
        banco_teste = Path(pasta) / "protecao.db"

        def conectar_teste():
            conexao = sqlite3.connect(banco_teste)
            conexao.execute("PRAGMA foreign_keys = ON")
            return conexao

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

            conexao.commit()

        def criar_compra(descricao):
            return CompraCartao(
                id=None,
                cartao_id=cartao_id,
                categoria_id=categoria_id,
                descricao=descricao,
                data_compra=date.today().isoformat(),
                valor_total=25990,
                quantidade_parcelas=1
            )

        hoje = date.today()
        fechamento_passado = (hoje - timedelta(days=1)).isoformat()
        fechamento_futuro = (hoje + timedelta(days=10)).isoformat()
        vencimento_futuro = (hoje + timedelta(days=15)).isoformat()

        with patch(
            "repositories.compra_cartao_repository.conectar",
            conectar_teste
        ):
            # TESTE 1: Fatura aberta com fechamento futuro
            compra = inserir_compra_com_parcela(
                criar_compra("Compra permitida"),
                "2030-01",
                fechamento_futuro,
                vencimento_futuro
            )

            assert compra.id is not None
            print("Teste 1: compra permitida OK")

            # TESTE 2: Fatura existente marcada como FECHADA
            with closing(conectar_teste()) as conexao:
                conexao.execute("""
                    INSERT INTO fatura (
                        cartao_id, mes_referencia,
                        data_fechamento, data_vencimento, status
                    )
                    VALUES (?, ?, ?, ?, 'FECHADA');
                """, (
                    cartao_id, "2030-02",
                    fechamento_futuro, vencimento_futuro
                ))
                conexao.commit()

            try:
                inserir_compra_com_parcela(
                    criar_compra("Compra bloqueada 1"),
                    "2030-02",
                    fechamento_futuro,
                    vencimento_futuro
                )
                raise AssertionError("Compra em fatura fechada foi aceita.")
            except ValueError:
                print("Teste 2: fatura fechada bloqueada OK")

            # TESTE 3: Fatura ABERTA com fechamento passado
            with closing(conectar_teste()) as conexao:
                conexao.execute("""
                    INSERT INTO fatura (
                        cartao_id, mes_referencia,
                        data_fechamento, data_vencimento, status
                    )
                    VALUES (?, ?, ?, ?, 'ABERTA');
                """, (
                    cartao_id, "2030-03",
                    fechamento_passado, vencimento_futuro
                ))
                conexao.commit()

            try:
                inserir_compra_com_parcela(
                    criar_compra("Compra bloqueada 2"),
                    "2030-03",
                    fechamento_passado,
                    vencimento_futuro
                )
                raise AssertionError("Compra após fechamento foi aceita.")
            except ValueError:
                print("Teste 3: data de fechamento protegida OK")

        with closing(conectar_teste()) as conexao:
            total = conexao.execute(
                "SELECT COUNT(*) FROM compra_cartao"
            ).fetchone()[0]

            assert total == 1

        print("Todos os testes de protecao passaram!")


if __name__ == "__main__":
    executar_teste()

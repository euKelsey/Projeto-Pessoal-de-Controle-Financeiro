
import sys
import tempfile
import sqlite3
from pathlib import Path
from unittest.mock import patch

RAIZ = Path(__file__).resolve().parent
sys.path.insert(0, str(RAIZ / "src"))

from database import conexao
from services.movimentacao_service import cadastrar_movimentacao


def executar_testes():
    with tempfile.TemporaryDirectory() as pasta:
        conexao.CAMINHO_BANCO = (
            Path(pasta) / "teste_seguranca.db"
        )

        conexao.inicializar_banco()

        banco = conexao.conectar()

        try:
            cursor = banco.cursor()

            cursor.execute("""
                INSERT INTO cartao (
                    nome, instituicao, limite_total,
                    dia_fechamento, dia_vencimento
                )
                VALUES ('Teste', 'Banco Teste', 100000, 5, 15);
            """)
            cartao_id = cursor.lastrowid

            cursor.execute("""
                INSERT INTO fatura (
                    cartao_id, mes_referencia,
                    data_fechamento, data_vencimento, status
                )
                VALUES (?, '2027-01', '2027-01-05',
                        '2027-01-15', 'ABERTA');
            """, (cartao_id,))
            fatura_id = cursor.lastrowid

            cursor.execute("""
                INSERT INTO lancamento (
                    tipo, descricao, valor_previsto,
                    data_prevista, fatura_id, origem
                )
                VALUES (
                    'DESPESA', 'Fatura de segurança',
                    25990, '2027-01-15', ?, 'FATURA'
                );
            """, (fatura_id,))
            lancamento_id = cursor.lastrowid

            banco.commit()

        finally:
            banco.close()

        # TESTE 1: impedir pagamento de fatura aberta.
        try:
            cadastrar_movimentacao(
                lancamento_id,
                25990,
                "2026-11-02",
                "PIX"
            )
        except ValueError as erro:
            assert "fechadas" in str(erro).lower()
            print("TESTE 1: Fatura aberta bloqueada OK")
        else:
            raise AssertionError(
                "Foi permitido pagar uma fatura aberta."
            )

        # Preparar a fatura fechada.
        banco = conexao.conectar()
        try:
            banco.execute("""
                UPDATE fatura
                SET status = 'FECHADA'
                WHERE id = ?;
            """, (fatura_id,))
            banco.commit()
        finally:
            banco.close()

        # TESTE 2: simular falha na atualização do lançamento.
        # O INSERT da movimentação deve ser desfeito.
        conexao_original = conexao.conectar

        def conectar_com_falha():
            banco = conexao_original()

            banco.execute("""
                CREATE TRIGGER IF NOT EXISTS teste_falha
                BEFORE UPDATE OF status ON lancamento
                BEGIN
                    SELECT RAISE(ABORT, 'Falha simulada');
                END;
            """)

            return banco

        with patch(
            "repositories.movimentacao_repository.conectar",
            side_effect=conectar_com_falha
        ):
            try:
                cadastrar_movimentacao(
                    lancamento_id,
                    25990,
                    "2026-11-02",
                    "PIX"
                )
            except sqlite3.DatabaseError as erro:
                assert "Falha simulada" in str(erro)
            else:
                raise AssertionError(
                    "A falha simulada não aconteceu."
                )

        banco = conexao.conectar()

        try:
            cursor = banco.cursor()

            cursor.execute("""
                SELECT COUNT(*)
                FROM movimentacao
                WHERE lancamento_id = ?;
            """, (lancamento_id,))

            quantidade = cursor.fetchone()[0]

            cursor.execute("""
                SELECT status
                FROM lancamento
                WHERE id = ?;
            """, (lancamento_id,))

            status = cursor.fetchone()[0]

            assert quantidade == 0
            assert status == "PENDENTE"

            print("TESTE 2: Rollback confirmado OK")
            print("TODOS OS TESTES DE SEGURANÇA PASSARAM!")

        finally:
            banco.close()


if __name__ == "__main__":
    executar_testes()

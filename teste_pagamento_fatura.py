
import sys
import tempfile
from pathlib import Path

# Permitir importar os modulos da pasta src.
RAIZ = Path(__file__).resolve().parent
sys.path.insert(0, str(RAIZ / "src"))

from database import conexao
from services.fatura_service import pagar_fatura


def testar_pagamento():
    # Criar um banco temporario para os testes.
    with tempfile.TemporaryDirectory() as pasta:
        conexao.CAMINHO_BANCO = (
            Path(pasta) / "teste_financeiro.db"
        )

        conexao.inicializar_banco()

        banco = conexao.conectar()

        try:
            cursor = banco.cursor()

            # Criar um cartao de teste.
            cursor.execute("""
                INSERT INTO cartao (
                    nome, instituicao, limite_total,
                    dia_fechamento, dia_vencimento
                )
                VALUES ('Teste', 'Banco Teste', 100000, 5, 15);
            """)

            cartao_id = cursor.lastrowid

            # Criar uma fatura fechada.
            cursor.execute("""
                INSERT INTO fatura (
                    cartao_id, mes_referencia,
                    data_fechamento, data_vencimento,
                    status
                )
                VALUES (?, '2026-10',
                        '2026-10-05', '2026-10-15',
                        'FECHADA');
            """, (cartao_id,))

            fatura_id = cursor.lastrowid

            # Criar o lancamento da fatura.
            cursor.execute("""
                INSERT INTO lancamento (
                    tipo, descricao, valor_previsto,
                    data_prevista, fatura_id, origem
                )
                VALUES (
                    'DESPESA', 'Fatura de teste',
                    25990, '2026-10-15', ?, 'FATURA'
                );
            """, (fatura_id,))

            lancamento_id = cursor.lastrowid

            # Criar outra fatura, ainda aberta.
            cursor.execute("""
                INSERT INTO fatura (
                    cartao_id, mes_referencia,
                    data_fechamento, data_vencimento,
                    status
                )
                VALUES (?, '2027-01',
                        '2027-01-05', '2027-01-15',
                        'ABERTA');
            """, (cartao_id,))

            fatura_aberta_id = cursor.lastrowid
            banco.commit()

        finally:
            banco.close()

        # TESTE 1 - Pagamento integral.
        pagar_fatura(
            fatura_id,
            "2026-11-02",
            "PIX"
        )

        banco = conexao.conectar()

        try:
            cursor = banco.cursor()

            cursor.execute("""
                SELECT valor
                FROM movimentacao
                WHERE lancamento_id = ?;
            """, (lancamento_id,))

            pagamento = cursor.fetchone()

            cursor.execute("""
                SELECT status
                FROM lancamento
                WHERE id = ?;
            """, (lancamento_id,))

            status = cursor.fetchone()[0]

            assert pagamento == (25990,)
            assert status == "EFETIVADO"

            print("TESTE 1: Pagamento integral OK")

        finally:
            banco.close()

        # TESTE 2 - Impedir pagamento duplicado.
        try:
            pagar_fatura(
                fatura_id,
                "2026-11-02",
                "PIX"
            )
        except ValueError:
            print("TESTE 2: Pagamento duplicado bloqueado OK")
        else:
            raise AssertionError(
                "O pagamento duplicado foi permitido!"
            )

        # TESTE 3 - Impedir pagamento de fatura aberta.
        try:
            pagar_fatura(
                fatura_aberta_id,
                "2026-11-02",
                "PIX"
            )
        except ValueError:
            print("TESTE 3: Fatura aberta bloqueada OK")
        else:
            raise AssertionError(
                "O pagamento de fatura aberta foi permitido!"
            )

        print("TODOS OS TESTES PASSARAM!")


if __name__ == "__main__":
    testar_pagamento()

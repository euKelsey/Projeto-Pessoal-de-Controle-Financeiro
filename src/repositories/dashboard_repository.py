
from database.conexao import conectar


def obter_resumo_mensal(mes_referencia: str) -> dict:
    # Definir o intervalo do mês.
    inicio = f"{mes_referencia}-01"

    ano, mes = map(int, mes_referencia.split("-"))

    if mes == 12:
        fim = f"{ano + 1}-01-01"
    else:
        fim = f"{ano}-{mes + 1:02d}-01"

    conexao = conectar()

    try:
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT
                COALESCE(SUM(
                    CASE WHEN tipo = 'RECEITA'
                    THEN valor_previsto ELSE 0 END
                ), 0),

                COALESCE(SUM(
                    CASE WHEN tipo = 'DESPESA'
                    THEN valor_previsto ELSE 0 END
                ), 0),

                COALESCE(SUM(
                    CASE
                        WHEN tipo = 'RECEITA'
                        AND status = 'EFETIVADO'
                        THEN valor_previsto ELSE 0
                    END
                ), 0),

                COALESCE(SUM(
                    CASE
                        WHEN tipo = 'DESPESA'
                        AND status = 'EFETIVADO'
                        THEN valor_previsto ELSE 0
                    END
                ), 0),

                COALESCE(SUM(
                    CASE
                        WHEN tipo = 'RECEITA'
                        AND status = 'PENDENTE'
                        THEN valor_previsto ELSE 0
                    END
                ), 0),

                COALESCE(SUM(
                    CASE
                        WHEN tipo = 'DESPESA'
                        AND status = 'PENDENTE'
                        THEN valor_previsto ELSE 0
                    END
                ), 0)

            FROM lancamento
            WHERE data_prevista >= ?
              AND data_prevista < ?
              AND status != 'CANCELADO';
        """, (inicio, fim))

        resultado = cursor.fetchone()

        receitas = resultado[0]
        despesas = resultado[1]

        return {
            "receitas": receitas,
            "despesas": despesas,
            "recebido": resultado[2],
            "pago": resultado[3],
            "a_receber": resultado[4],
            "a_pagar": resultado[5],
            "saldo_previsto": receitas - despesas
        }

    finally:
        conexao.close()
        

def listar_proximos_vencimentos(
    data_limite: str,
    quantidade: int = 10
) -> list:
    conexao = conectar()

    try:
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT
                id,
                descricao,
                valor_previsto,
                data_prevista,
                origem
            FROM lancamento
            WHERE tipo = 'DESPESA'
              AND status = 'PENDENTE'
              AND data_prevista <= ?
            ORDER BY data_prevista ASC, id ASC
            LIMIT ?;
        """, (data_limite, quantidade))

        registros = cursor.fetchall()

        vencimentos = []

        for registro in registros:
            vencimentos.append({
                "id": registro[0],
                "descricao": registro[1],
                "valor": registro[2],
                "data_vencimento": registro[3],
                "origem": registro[4]
            })

        return vencimentos

    finally:
        conexao.close()


def listar_resumo_faturas(quantidade: int = 6) -> list:
    conexao = conectar()

    try:
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT
                f.id,
                c.nome,
                f.mes_referencia,
                f.data_vencimento,
                f.status,
                COALESCE((
                    SELECT SUM(p.valor)
                    FROM parcela_cartao AS p
                    INNER JOIN compra_cartao AS cc
                        ON cc.id = p.compra_cartao_id
                    WHERE p.fatura_id = f.id
                      AND cc.status = 'ATIVA'
                ), 0) AS total,
                l.status AS status_lancamento

            FROM fatura AS f

            INNER JOIN cartao AS c
                ON c.id = f.cartao_id

            LEFT JOIN lancamento AS l
                ON l.fatura_id = f.id

            WHERE (
                l.id IS NULL
                OR l.status = 'PENDENTE'
            )

            AND EXISTS (
                SELECT 1
                FROM parcela_cartao AS p
                INNER JOIN compra_cartao AS cc
                    ON cc.id = p.compra_cartao_id
                WHERE p.fatura_id = f.id
                  AND cc.status = 'ATIVA'
            )

            ORDER BY f.data_vencimento ASC, f.id ASC
            LIMIT ?;
        """, (quantidade,))

        registros = cursor.fetchall()

        faturas = []

        for registro in registros:
            if registro[5] <= 0:
                continue

            faturas.append({
                "id": registro[0],
                "cartao": registro[1],
                "mes_referencia": registro[2],
                "vencimento": registro[3],
                "status": registro[4],
                "total": registro[5],
                "status_lancamento": registro[6]
            })

        return faturas

    finally:
        conexao.close()


def obter_total_compras_cartao(mes_referencia: str) -> int:
    conexao = conectar()

    try:
        cursor = conexao.cursor()

        # Definir o início do mês selecionado
        data_inicio = f"{mes_referencia}-01"

        # Consultar compras realizadas no mês
        cursor.execute("""
            SELECT COALESCE(SUM(valor_total), 0)
            FROM compra_cartao
            WHERE status = 'ATIVA'
              AND substr(data_compra, 1, 7) = ?;
        """, (mes_referencia,))

        total = cursor.fetchone()[0]

        return total

    finally:
        conexao.close()


def obter_total_despesas_comuns(
    mes_referencia: str
) -> int:

    conexao = conectar()

    try:
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT COALESCE(
                SUM(valor_previsto), 0
            )
            FROM lancamento

            WHERE tipo = 'DESPESA'

              AND origem != 'FATURA'

              AND status != 'CANCELADO'

              AND substr(data_prevista, 1, 7) = ?;

        """, (mes_referencia,))

        total = cursor.fetchone()[0]

        return total

    finally:
        conexao.close()


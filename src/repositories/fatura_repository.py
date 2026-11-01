from database.conexao import conectar
from models.fatura import Fatura
from datetime import date

def inserir(fatura: Fatura):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO fatura (
            cartao_id,
            mes_referencia,
            data_fechamento,
            data_vencimento,
            status
        )
        VALUES (?, ?, ?, ?, ?);
    """, (
        fatura.cartao_id,
        fatura.mes_referencia,
        fatura.data_fechamento,
        fatura.data_vencimento,
        fatura.status
    ))

    conexao.commit()

    fatura.id = cursor.lastrowid

    conexao.close()

    return fatura

def listar():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            id,
            cartao_id,
            mes_referencia,
            data_fechamento,
            data_vencimento,
            status
        FROM fatura
        ORDER BY mes_referencia;
    """)

    registros = cursor.fetchall()

    faturas = []

    for registro in registros:
        fatura = Fatura(
            id=registro[0],
            cartao_id=registro[1],
            mes_referencia=registro[2],
            data_fechamento=registro[3],
            data_vencimento=registro[4],
            status=registro[5]
        )

        faturas.append(fatura)

    conexao.close()

    return faturas

def buscar_por_id(fatura_id: int):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            id,
            cartao_id,
            mes_referencia,
            data_fechamento,
            data_vencimento,
            status
        FROM fatura
        WHERE id = ?;
    """, (fatura_id,))

    registro = cursor.fetchone()

    conexao.close()

    if registro is None:
        return None

    return Fatura(
        id=registro[0],
        cartao_id=registro[1],
        mes_referencia=registro[2],
        data_fechamento=registro[3],
        data_vencimento=registro[4],
        status=registro[5]
    )
    
def atualizar(fatura: Fatura):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE fatura
        SET
            cartao_id = ?,
            mes_referencia = ?,
            data_fechamento = ?,
            data_vencimento = ?,
            status = ?
        WHERE id = ?;
    """, (
        fatura.cartao_id,
        fatura.mes_referencia,
        fatura.data_fechamento,
        fatura.data_vencimento,
        fatura.status,
        fatura.id
    ))

    conexao.commit()
    conexao.close()

    return fatura

def buscar_por_cartao_mes(cartao_id: int, mes_referencia: str):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            id,
            cartao_id,
            mes_referencia,
            data_fechamento,
            data_vencimento,
            status
        FROM fatura
        WHERE cartao_id = ?
          AND mes_referencia = ?;
    """, (
        cartao_id,
        mes_referencia
    ))

    registro = cursor.fetchone()

    conexao.close()

    if registro is None:
        return None

    return Fatura(
        id=registro[0],
        cartao_id=registro[1],
        mes_referencia=registro[2],
        data_fechamento=registro[3],
        data_vencimento=registro[4],
        status=registro[5]
    )
    

def calcular_total_fatura(fatura_id: int) -> int:
    conexao = conectar()

    try:
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT COALESCE(SUM(p.valor), 0)
            FROM parcela_cartao AS p
            INNER JOIN compra_cartao AS c
                ON c.id = p.compra_cartao_id
            WHERE p.fatura_id = ?
              AND c.status = 'ATIVA';
        """, (fatura_id,))

        resultado = cursor.fetchone()

        return resultado[0]

    finally:
        conexao.close()

def fechar_fatura(fatura_id: int) -> bool:
    conexao = conectar()

    try:
        cursor = conexao.cursor()

        cursor.execute("""
            UPDATE fatura
            SET status = 'FECHADA'
            WHERE id = ?
              AND status = 'ABERTA';
        """, (fatura_id,))

        alterou = cursor.rowcount > 0

        conexao.commit()

        return alterou

    except Exception:
        conexao.rollback()
        raise

    finally:
        conexao.close()
        

def fechar_faturas_vencidas(data_referencia: str | None = None) -> int:
    if data_referencia is None:
        data_referencia = date.today().isoformat()

    conexao = conectar()

    try:
        cursor = conexao.cursor()

        cursor.execute("""
            UPDATE fatura
            SET status = 'FECHADA'
            WHERE status = 'ABERTA'
              AND data_fechamento <= ?;
        """, (data_referencia,))

        quantidade_fechada = cursor.rowcount

        conexao.commit()

        return quantidade_fechada

    except Exception:
        conexao.rollback()
        raise

    finally:
        conexao.close()

def gerar_lancamento_fatura(fatura_id: int) -> int | None:
    conexao = conectar()

    try:
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT
                mes_referencia,
                data_vencimento,
                status
            FROM fatura
            WHERE id = ?;
        """, (fatura_id,))

        fatura = cursor.fetchone()

        if fatura is None:
            raise ValueError("Fatura não encontrada.")

        mes_referencia, vencimento, status = fatura

        if status != "FECHADA":
            raise ValueError(
                "A fatura precisa estar fechada."
            )

        cursor.execute("""
            SELECT id
            FROM lancamento
            WHERE fatura_id = ?;
        """, (fatura_id,))

        existente = cursor.fetchone()

        if existente is not None:
            return existente[0]

        cursor.execute("""
            SELECT COALESCE(SUM(p.valor), 0)
            FROM parcela_cartao AS p
            INNER JOIN compra_cartao AS c
                ON c.id = p.compra_cartao_id
            WHERE p.fatura_id = ?
              AND c.status = 'ATIVA';
        """, (fatura_id,))

        total = cursor.fetchone()[0]

        if total <= 0:
            return None

        cursor.execute("""
            INSERT INTO lancamento (
                tipo,
                descricao,
                valor_previsto,
                data_prevista,
                categoria_id,
                fatura_id,
                status,
                origem
            )
            VALUES (
                'DESPESA',
                ?,
                ?,
                ?,
                NULL,
                ?,
                'PENDENTE',
                'FATURA'
            );
        """, (
            f"Fatura do cartão - {mes_referencia}",
            total,
            vencimento,
            fatura_id
        ))

        lancamento_id = cursor.lastrowid
        conexao.commit()

        return lancamento_id

    except Exception:
        conexao.rollback()
        raise

    finally:
        conexao.close()
        

def processar_faturas_automaticamente(
    data_referencia: str
) -> tuple[int, int]:
    conexao = conectar()

    try:
        cursor = conexao.cursor()

        # 1. Fechar as faturas cuja data chegou.
        cursor.execute("""
            UPDATE fatura
            SET status = 'FECHADA'
            WHERE status = 'ABERTA'
              AND data_fechamento <= ?;
        """, (data_referencia,))

        quantidade_fechada = cursor.rowcount

        # 2. Encontrar faturas fechadas sem lançamento.

        cursor.execute("""
            SELECT
                f.id,
                f.mes_referencia,
                f.data_vencimento,
                COALESCE((
                    SELECT SUM(p.valor)
                    FROM parcela_cartao AS p
                    INNER JOIN compra_cartao AS c
                        ON c.id = p.compra_cartao_id
                    WHERE p.fatura_id = f.id
                      AND c.status = 'ATIVA'
                ), 0) AS total
            FROM fatura AS f
            WHERE f.status = 'FECHADA'
              AND NOT EXISTS (
                  SELECT 1
                  FROM lancamento AS l
                  WHERE l.fatura_id = f.id
              );
        """)

        faturas = cursor.fetchall()
        quantidade_lancamentos = 0

        # 3. Criar os lançamentos pendentes.
        for fatura_id, mes, vencimento, total in faturas:
            if total <= 0:
                continue

            cursor.execute("""
                INSERT INTO lancamento (
                    tipo,
                    descricao,
                    valor_previsto,
                    data_prevista,
                    categoria_id,
                    fatura_id,
                    status,
                    origem
                )
                VALUES (
                    'DESPESA',
                    ?, ?, ?, NULL, ?,
                    'PENDENTE', 'FATURA'
                );
            """, (
                f"Fatura do cartão - {mes}",
                total,
                vencimento,
                fatura_id
            ))

            quantidade_lancamentos += 1

        conexao.commit()

        return quantidade_fechada, quantidade_lancamentos

    except Exception:
        conexao.rollback()
        raise

    finally:
        conexao.close()

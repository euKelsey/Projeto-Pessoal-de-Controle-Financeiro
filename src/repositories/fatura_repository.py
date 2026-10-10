from database.conexao import conectar
from models.fatura import Fatura

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
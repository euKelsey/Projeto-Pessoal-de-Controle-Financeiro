from database.conexao import conectar
from models.movimentacao import Movimentacao

def inserir(movimentacao: Movimentacao):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO movimentacao (
            lancamento_id,
            valor,
            data_movimentacao,
            forma,
            observacao
        )
        VALUES (?, ?, ?, ?, ?);
    """, (
        movimentacao.lancamento_id,
        movimentacao.valor,
        movimentacao.data_movimentacao,
        movimentacao.forma,
        movimentacao.observacao
    ))

    conexao.commit()

    movimentacao.id = cursor.lastrowid

    conexao.close()

    return movimentacao

def listar():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            id,
            lancamento_id,
            valor,
            data_movimentacao,
            forma,
            observacao
        FROM movimentacao
        ORDER BY data_movimentacao;
    """)

    registros = cursor.fetchall()

    movimentacoes = []

    for registro in registros:
        movimentacao = Movimentacao(
            id=registro[0],
            lancamento_id=registro[1],
            valor=registro[2],
            data_movimentacao=registro[3],
            forma=registro[4],
            observacao=registro[5]
        )

        movimentacoes.append(movimentacao)

    conexao.close()

    return movimentacoes

def buscar_por_id(movimentacao_id: int):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            id,
            lancamento_id,
            valor,
            data_movimentacao,
            forma,
            observacao
        FROM movimentacao
        WHERE id = ?;
    """, (movimentacao_id,))

    registro = cursor.fetchone()

    conexao.close()

    if registro is None:
        return None

    return Movimentacao(
        id=registro[0],
        lancamento_id=registro[1],
        valor=registro[2],
        data_movimentacao=registro[3],
        forma=registro[4],
        observacao=registro[5]
    )
    
def atualizar(movimentacao: Movimentacao):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE movimentacao
        SET
            lancamento_id = ?,
            valor = ?,
            data_movimentacao = ?,
            forma = ?,
            observacao = ?
        WHERE id = ?;
    """, (
        movimentacao.lancamento_id,
        movimentacao.valor,
        movimentacao.data_movimentacao,
        movimentacao.forma,
        movimentacao.observacao,
        movimentacao.id
    ))

    conexao.commit()
    conexao.close()

    return movimentacao

def buscar_por_lancamento_id(lancamento_id: int):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            id,
            lancamento_id,
            valor,
            data_movimentacao,
            forma,
            observacao
        FROM movimentacao
        WHERE lancamento_id = ?;
    """, (lancamento_id,))

    registro = cursor.fetchone()

    conexao.close()

    if registro is None:
        return None

    return Movimentacao(
        id=registro[0],
        lancamento_id=registro[1],
        valor=registro[2],
        data_movimentacao=registro[3],
        forma=registro[4],
        observacao=registro[5]
    )
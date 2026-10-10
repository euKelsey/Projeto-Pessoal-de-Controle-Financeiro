from database.conexao import conectar 
from models.lancamento import Lancamento 

def inserir(lancamento: Lancamento):
    conexao = conectar()
    cursor = conexao.cursor()
    
    cursor.execute("""
        INSERT INTO lancamento (
            tipo,
            descricao,
            valor_previsto,
            data_prevista,
            categoria_id,
            recorrencia_id,
            fatura_id,
            status,
            observacao,
            origem
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, (
        lancamento.tipo,
        lancamento.descricao,
        lancamento.valor_previsto,
        lancamento.data_prevista,
        lancamento.categoria_id,
        lancamento.recorrencia_id,
        lancamento.fatura_id,
        lancamento.status,
        lancamento.observacao,
        lancamento.origem
    ))
    
    conexao.commit()
    
    lancamento.id = cursor.lastrowid 
    
    conexao.close()
    
    return lancamento 

def listar():
    conexao = conectar()
    cursor = conexao.cursor()
    
    cursor.execute("""
        SELECT
            id,
            tipo,
            descricao,
            valor_previsto,
            data_prevista,
            categoria_id,
            recorrencia_id,
            fatura_id,
            status,
            observacao,
            origem
        FROM lancamento
        ORDER BY data_prevista;
    """)
    
    registros = cursor.fetchall()
    
    lancamentos = []
    
    for registro in registros:
        lancamento = Lancamento(
            id=registro[0],
            tipo=registro[1],
            descricao=registro[2],
            valor_previsto=registro[3],
            data_prevista=registro[4],
            categoria_id=registro[5],
            recorrencia_id=registro[6],
            fatura_id=registro[7],
            status=registro[8],
            observacao=registro[9],
            origem=registro[10]
        )
        
        lancamentos.append(lancamento)
        
    conexao.close()
    
    return lancamentos

def buscar_por_id(lancamento_id: int):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            id,
            tipo,
            descricao,
            valor_previsto,
            data_prevista,
            categoria_id,
            recorrencia_id,
            fatura_id,
            status,
            observacao,
            origem
        FROM lancamento
        WHERE id = ?;
    """, (lancamento_id,))

    registro = cursor.fetchone()

    conexao.close()

    if registro is None:
        return None

    return Lancamento(
        id=registro[0],
        tipo=registro[1],
        descricao=registro[2],
        valor_previsto=registro[3],
        data_prevista=registro[4],
        categoria_id=registro[5],
        recorrencia_id=registro[6],
        fatura_id=registro[7],
        status=registro[8],
        observacao=registro[9],
        origem=registro[10]
    )
    
def atualizar(lancamento: Lancamento):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE lancamento
        SET
            tipo = ?,
            descricao = ?,
            valor_previsto = ?,
            data_prevista = ?,
            categoria_id = ?,
            recorrencia_id = ?,
            fatura_id = ?,
            status = ?,
            observacao = ?,
            origem = ?
        WHERE id = ?;
    """, (
        lancamento.tipo,
        lancamento.descricao,
        lancamento.valor_previsto,
        lancamento.data_prevista,
        lancamento.categoria_id,
        lancamento.recorrencia_id,
        lancamento.fatura_id,
        lancamento.status,
        lancamento.observacao,
        lancamento.origem,
        lancamento.id
    ))

    conexao.commit()
    conexao.close()

    return lancamento

def cancelar(lancamento_id: int):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE lancamento
        SET status = 'CANCELADO'
        WHERE id = ?;
    """, (lancamento_id,))

    conexao.commit()
    conexao.close()
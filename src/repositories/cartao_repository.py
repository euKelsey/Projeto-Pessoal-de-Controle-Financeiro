from database.conexao import conectar
from models.cartao import Cartao

def inserir(cartao: Cartao):
    conexao = conectar()
    cursor = conexao.cursor()
    
    cursor.execute("""
        INSERT INTO cartao (
            nome,
            instituicao,
            limite_total,
            dia_fechamento,
            dia_vencimento,
            status,
            observacao
        )
        VALUES (?, ?, ?, ?, ?, ?, ?);
    """, (
        cartao.nome,
        cartao.instituicao,
        cartao.limite_total,
        cartao.dia_fechamento,
        cartao.dia_vencimento,
        cartao.status,
        cartao.observacao
        
    ))
        
    conexao.commit()
    
    cartao.id = cursor.lastrowid
    
    conexao.close()
    
    return cartao

def listar():
    conexao = conectar()
    cursor = conexao.cursor()
    
    cursor.execute("""
        SELECT
            id,
            nome,
            instituicao,
            limite_total,
            dia_fechamento,
            dia_vencimento,
            status,
            observacao
        FROM cartao 
        ORDER BY nome;
    """)
    
    registros = cursor.fetchall()
    
    cartoes = []
    
    for registro in registros:
        cartao = Cartao(
            id=registro[0],
            nome=registro[1],
            instituicao=registro[2],
            limite_total=registro[3],
            dia_fechamento=registro[4],
            dia_vencimento=registro[5],
            status=registro[6],
            observacao=registro[7]
        )
        
        cartoes.append(cartao)
        
    conexao.close()
    
    return cartoes 

def buscar_por_id(cartao_id: int):
    conexao = conectar()
    cursor = conexao.cursor()
    
    cursor.execute("""
        SELECT
            id,
            nome,
            instituicao,
            limite_total,
            dia_fechamento,
            dia_vencimento,
            status,
            observacao
        FROM cartao 
        WHERE id = ?;
    """, (cartao_id,))
    
    registro = cursor.fetchone()
    
    conexao.close()
    
    if registro is None:
        return None
    
    return Cartao(
        id=registro[0],
        nome=registro[1],
        instituicao=registro[2],
        limite_total=registro[3],
        dia_fechamento=registro[4],
        dia_vencimento=registro[5],
        status=registro[6],
        observacao=registro[7]
    )
    
def atualizar(cartao: Cartao):
    conexao = conectar()
    cursor = conexao.cursor()
    
    cursor.execute("""
        UPDATE cartao
        SET 
            nome = ?,
            instituicao = ?,
            limite_total = ?,
            dia_fechamento = ?,
            dia_vencimento = ?,
            status = ?,
            observacao = ?
        WHERE id = ?;
    """, (
        cartao.nome,
        cartao.instituicao,
        cartao.limite_total,
        cartao.dia_fechamento,
        cartao.dia_vencimento,
        cartao.status,
        cartao.observacao,
        cartao.id
    ))
    
    conexao.commit()
    conexao.close()
    
    return cartao 

def inativar(cartao_id: int):
    conexao = conectar()
    cursor = conexao.cursor()
    
    cursor.execute("""
        UPDATE cartao
        SET status = 'INATIVO'
        WHERE id = ?;
    """, (cartao_id,))
    
    conexao.commit()
    conexao.close()
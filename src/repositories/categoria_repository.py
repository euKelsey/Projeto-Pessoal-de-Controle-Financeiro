from database.conexao import conectar
from models.categoria import Categoria

def inserir(categoria: Categoria):
    conexao = conectar()
    cursor = conexao.cursor()
    
    cursor.execute("""
        INSERT INTO categoria (
            nome,
            tipo,
            descricao,
            status
        )
        VALUES (?, ?, ?, ?);
    """, (
        categoria.nome,
        categoria.tipo,
        categoria.descricao,
        categoria.status    
    ))
    
    conexao.commit()
    
    categoria.id = cursor.lastrowid
    
    conexao.close()
    
    return categoria

def listar():
    conexao = conectar()
    cursor = conexao.cursor()
    
    cursor.execute("""
        SELECT
            id,
            nome,
            tipo,
            descricao,
            status
        FROM categoria
        ORDER BY nome;
    """)
    
    registros = cursor.fetchall()
    
    categorias = []
    
    for registro in registros:
        categoria = Categoria(
            id=registro[0],
            nome=registro[1],
            tipo=registro[2],
            descricao=registro[3],
            status=registro[4]
        )
        
        categorias.append(categoria)
        
    conexao.close()
    
    return categorias

def buscar_por_id(categoria_id: int):
    conexao = conectar()
    cursor = conexao.cursor()
    
    cursor.execute("""
        SELECT
            id,
            nome,
            tipo,
            descricao,
            status
        FROM categoria
        WHERE id = ?;
    """, (categoria_id,))
    
    registro = cursor.fetchone()
    
    conexao.close()
    
    if registro is None:
        return None
    
    categoria = Categoria(
        id=registro[0],
        nome=registro[1],
        tipo=registro[2],
        descricao=registro[3],
        status=registro[4]
    )
    
    return categoria

def atualizar(categoria: Categoria):
    conexao = conectar()

    try:
        cursor = conexao.cursor()

        cursor.execute("""
            UPDATE categoria
            SET
                nome = ?,
                tipo = ?,
                descricao = ?,
                status = ?
            WHERE id = ?;
        """, (
            categoria.nome,
            categoria.tipo,
            categoria.descricao,
            categoria.status,
            categoria.id
        ))

        conexao.commit()

        return categoria

    except Exception:
        conexao.rollback()
        raise

    finally:
        conexao.close()

def inativar(categoria_id: int):
    conexao = conectar()
    cursor = conexao.cursor()
    
    cursor.execute("""
        UPDATE categoria
        SET status = 'INATIVA'
        WHERE id = ?;
    """, (categoria_id,))
    
    conexao.commit()
    conexao.close()
    
def listar_ativas():
    conexao = conectar()
    cursor = conexao.cursor()
    
    cursor.execute("""
        SELECT
            id,
            nome,
            tipo,
            descricao,
            status
        FROM Categoria
        WHERE status = 'ATIVA'
        ORDER BY nome;
    """)
    
    registros = cursor.fetchall()
    
    categorias = []
    
    for registro in registros:
        categoria = Categoria(
            id=registro[0],
            nome=registro[1],
            tipo=registro[2],
            descricao=registro[3],
            status=registro[4]
        )
        
        categorias.append(categoria)
        
    conexao.close()
    
    return categorias

def buscar_por_nome_tipo(nome: str, tipo: str):
    conexao = conectar()
    cursor = conexao.cursor()
    
    cursor.execute("""
        SELECT
        id,
        nome,
        tipo,
        descricao,
        status
    FROM Categoria
    WHERE nome = ? AND tipo = ?;
    """, (nome, tipo))
    
    registro = cursor.fetchone()
    
    conexao.close()
    
    if registro is None:
        return None
    
    return Categoria(
        id=registro[0],
        nome=registro[1],
        tipo=registro[2],
        descricao=registro[3],
        status=registro[4]
    )
from models.categoria import Categoria
from repositories.categoria_repository import (
    inserir,
    listar,
    listar_ativas,
    buscar_por_id,
    atualizar,
    inativar,
    buscar_por_nome_tipo
)

def cadastrar_categoria(nome: str, tipo: str, descricao: str | None = None):
    nome = nome.strip()
    tipo = tipo.strip().upper()
    
    if not nome:
        raise ValueError("O nome da categoria é obrigatório.")
    
    if tipo not in ("RECEITA", "DESPESA"):
        raise ValueError("O tipo da categoria deve ser RECEITA ou DESPESA.")
    
    categoria_existente = buscar_por_nome_tipo(nome, tipo)
    
    if categoria_existente is not None:
        raise ValueError(
            "Já existe uma categoria com esse nome e tipo."
        )
    
    categoria = Categoria(
        id=None,
        nome=nome,
        tipo=tipo,
        descricao=descricao
    )
    
    return inserir(categoria)

def listar_categorias():
    return listar()

def listar_categorias_ativas():
    return listar_ativas()

def atualizar_categoria(
    categoria_id: int,
    nome: str,
    tipo: str,
    descricao: str | None = None,
    status: str = "ATIVA"
):
    categoria = buscar_por_id(categoria_id)
    
    if categoria is None:
        raise ValueError("Categoria não encontrada.")
    
    nome = nome.strip()
    tipo = tipo.strip().upper()
    status = status.strip().upper()
    
    if not nome:
        raise ValueError("O nome da categoria é obrigatorio.")
    
    if tipo not in ("RECEITA", "DESPESA"):
        raise ValueError("O status deve ser ATIVA ou INATIVA.")
    
    categoria.nome = nome
    categoria.tipo = tipo 
    categoria.descricao = descricao 
    categoria.status = status 
    
    return atualizar(categoria)

def inativar_categoria(categoria_id: int):
    categoria = buscar_por_id(categoria_id)
    
    if categoria is None:
        raise ValueError("Categoria não encontrada.")
    
    inativar(categoria_id)
    
    return buscar_por_id(categoria_id)


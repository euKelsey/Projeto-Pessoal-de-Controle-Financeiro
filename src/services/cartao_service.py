from models.cartao import Cartao
from repositories.cartao_repository import (
    inserir,
    listar,
    buscar_por_id,
    atualizar,
    inativar
)


def cadastrar_cartao(
    nome: str,
    instituicao: str,
    limite_total: int,
    dia_fechamento: int,
    dia_vencimento: int,
    observacao: str | None = None
):
    nome = nome.strip()
    instituicao = instituicao.strip()

    if not nome:
        raise ValueError("O nome do cartão é obrigatório.")

    if not instituicao:
        raise ValueError("A instituião do cartão é obrigatória.")

    if limite_total < 0:
        raise ValueError("O limite total não pode ser negativo.")
    
    if not 1 <= dia_fechamento <= 31:
        raise ValueError("O dia de fechamento deve estar entre 1 e 31.")

    if not 1 <= dia_vencimento <= 31:
        raise ValueError("O dia de vencimento deve estar entre 1 e 31.")

    cartao = Cartao(
        id=None,
        nome=nome,
        instituicao=instituicao,
        limite_total=limite_total,
        dia_fechamento=dia_fechamento,
        dia_vencimento=dia_vencimento,
        observacao=observacao
    )

    return inserir(cartao)


def listar_cartoes():
    return listar()


def buscar_cartao_por_id(cartao_id: int):
    cartao = buscar_por_id(cartao_id)

    if cartao is None:
        raise ValueError("Cartão não encontrado.")

    return cartao


def atualizar_cartao(
    cartao_id: int,
    nome: str,
    instituicao: str,
    limite_total: int,
    dia_fechamento: int,
    dia_vencimento: int,
    status: str = "ATIVO",
    observacao: str | None = None
):
    cartao = buscar_por_id(cartao_id)

    if cartao is None:
        raise ValueError("Cartão não encontrado.")

    nome = nome.strip()
    instituicao = instituicao.strip()
    status = status.strip().upper()

    if not nome:
        raise ValueError("O nome do cartão é obrigatório.")

    if not instituicao:
        raise ValueError("A instituição do cartão é obrigatória.")

    if limite_total < 0:
        raise ValueError("O limite total não pode ser negativo.")

    if not 1 <= dia_fechamento <= 31:
        raise ValueError("O dia de fechamento deve estar entre 1 e 31.")

    if not 1 <= dia_vencimento <= 31:
        raise ValueError("O dia de vencimento deve estar entre 1 e 31.")

    if status not in ("ATIVO", "INATIVO"):
        raise ValueError("O status deve ser ATIVO ou INATIVO.")

    cartao.nome = nome
    cartao.instituicao = instituicao
    cartao.limite_total = limite_total
    cartao.dia_fechamento = dia_fechamento
    cartao.dia_vencimento = dia_vencimento
    cartao.status = status
    cartao.observacao = observacao

    return atualizar(cartao)

def inativar_cartao(cartao_id: int):
    cartao = buscar_por_id(cartao_id)

    if cartao is None:
        raise ValueError("Cartão não encontrado.")

    inativar(cartao_id)

    return buscar_por_id(cartao_id)
from models.movimentacao import Movimentacao
from repositories.lancamento_repository import (
    buscar_por_id as buscar_lancamento_por_id,
    atualizar as atualizar_lancamento
)
from repositories.lancamento_repository import buscar_por_id as buscar_lancamento_por_id
from repositories.movimentacao_repository import (
    inserir,
    listar,
    buscar_por_id,
    buscar_por_lancamento_id,
    atualizar
)
from repositories.lancamento_repository import buscar_por_id as buscar_lancamento_por_id


def cadastrar_movimentacao(
    lancamento_id: int,
    valor: int,
    data_movimentacao: str,
    forma: str,
    observacao: str | None = None
):
    forma = forma.strip().upper()

    lancamento = buscar_lancamento_por_id(lancamento_id)

    if lancamento is None:
        raise ValueError("Lançamento não encontrado.")

    if valor <= 0:
        raise ValueError("O valor da movimentação deve ser maior que zero.")

    formas_validas = (
        "PIX",
        "DINHEIRO",
        "DEBITO",
        "TRANSFERENCIA",
        "BOLETO",
        "OUTRO"
    )

    if forma not in formas_validas:
        raise ValueError("Forma de movimentação inválida.")

    movimentacao_existente = buscar_por_lancamento_id(lancamento_id)

    if movimentacao_existente is not None:
        raise ValueError("Este lançamento já possui uma movimentação.")

    movimentacao = Movimentacao(
        id=None,
        lancamento_id=lancamento_id,
        valor=valor,
        data_movimentacao=data_movimentacao,
        forma=forma,
        observacao=observacao
    )

    movimentacao_salva = inserir(movimentacao)

    lancamento.status = "EFETIVADO"
    atualizar_lancamento(lancamento)

    return movimentacao_salva

def listar_movimentacoes():
    return listar()


def buscar_movimentacao_por_id(movimentacao_id: int):
    movimentacao = buscar_por_id(movimentacao_id)

    if movimentacao is None:
        raise ValueError("Movimentação não encontrada.")

    return movimentacao

def atualizar_movimentacao(
    movimentacao_id: int,
    valor: int,
    data_movimentacao: str,
    forma: str,
    observacao: str | None = None
):
    movimentacao = buscar_por_id(movimentacao_id)

    if movimentacao is None:
        raise ValueError("Movimentação não encontrada.")

    forma = forma.strip().upper()

    if valor <= 0:
        raise ValueError("O valor da movimentação deve ser maior que zero.")

    formas_validas = (
        "PIX",
        "DINHEIRO",
        "DEBITO",
        "TRANSFERENCIA",
        "BOLETO",
        "OUTRO"
    )

    if forma not in formas_validas:
        raise ValueError("Forma de movimentação inválida.")

    movimentacao.valor = valor
    movimentacao.data_movimentacao = data_movimentacao
    movimentacao.forma = forma
    movimentacao.observacao = observacao

    return atualizar(movimentacao)

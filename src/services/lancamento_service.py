from models.lancamento import Lancamento
from repositories.lancamento_repository import (
    inserir,
    listar,
    buscar_por_id,
    atualizar,
    cancelar
)

def cadastrar_lancamento(
    tipo: str,
    descricao: str,
    valor_previsto: int,
    data_prevista: str,
    categoria_id: int,
    observacao: str | None = None
):
    tipo = tipo.strip().upper()
    descricao = descricao.strip()

    if tipo not in ("RECEITA", "DESPESA"):
        raise ValueError("O tipo deve ser RECEITA ou DESPESA.")

    if not descricao:
        raise ValueError("A descrição é obrigatória.")

    if valor_previsto <= 0:
        raise ValueError("O valor previsto deve ser maior que zero.")

    if categoria_id is None:
        raise ValueError("A categoria é obrigatória.")

    lancamento = Lancamento(
        id=None,
        tipo=tipo,
        descricao=descricao,
        valor_previsto=valor_previsto,
        data_prevista=data_prevista,
        categoria_id=categoria_id,
        observacao=observacao,
        origem="MANUAL"
    )

    return inserir(lancamento)

def listar_lancamentos():
    return listar()

def buscar_lancamento_por_id(lancamento_id: int):
    lancamento = buscar_por_id(lancamento_id)

    if lancamento is None:
        raise ValueError("Lançamento não encontrado.")

    return lancamento

def atualizar_lancamento(
    lancamento_id: int,
    tipo: str,
    descricao: str,
    valor_previsto: int,
    data_prevista: str,
    categoria_id: int,
    status: str = "PENDENTE",
    observacao: str | None = None
):
    lancamento = buscar_por_id(lancamento_id)

    if lancamento is None:
        raise ValueError("Lançamento não encontrado.")

    tipo = tipo.strip().upper()
    descricao = descricao.strip()
    status = status.strip().upper()

    if tipo not in ("RECEITA", "DESPESA"):
        raise ValueError("O tipo deve ser RECEITA ou DESPESA.")

    if not descricao:
        raise ValueError("A descrição é obrigatória.")

    if valor_previsto <= 0:
        raise ValueError("O valor previsto deve ser maior que zero.")

    if categoria_id is None:
        raise ValueError("A categoria é obrigatória.")

    if status not in ("PENDENTE", "EFETIVADO", "CANCELADO"):
        raise ValueError(
            "O status deve ser PENDENTE, EFETIVADO ou CANCELADO."
        )

    lancamento.tipo = tipo
    lancamento.descricao = descricao
    lancamento.valor_previsto = valor_previsto
    lancamento.data_prevista = data_prevista
    lancamento.categoria_id = categoria_id
    lancamento.status = status
    lancamento.observacao = observacao

    return atualizar(lancamento)

def cancelar_lancamento(lancamento_id: int):
    lancamento = buscar_por_id(lancamento_id)

    if lancamento is None:
        raise ValueError("Lançamento não encontrado.")

    cancelar(lancamento_id)

    return buscar_por_id(lancamento_id)
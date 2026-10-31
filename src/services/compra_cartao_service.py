from repositories.compra_cartao_repository import (
    listar,
    buscar_por_id,
    inserir_compra_com_parcela
)

from services.competencia_fatura_service import (
    calcular_mes_fatura,
    calcular_datas_fatura
)

from repositories.fatura_repository import (
    buscar_por_cartao_mes
)

from datetime import datetime

from models.compra_cartao import CompraCartao

from repositories.cartao_repository import (
    buscar_por_id as buscar_cartao_por_id
)

from repositories.categoria_repository import (
    buscar_por_id as buscar_categoria_por_id
)

def listar_compras():
    return listar()


def buscar_compra_por_id(compra_id: int):
    compra = buscar_por_id(compra_id)

    if compra is None:
        raise ValueError("Compra não encontrada.")

    return compra

def cadastrar_compra(
    cartao_id: int,
    categoria_id: int,
    descricao: str,
    data_compra: str,
    valor_total: int,
    observacao: str | None = None
):
    cartao = buscar_cartao_por_id(cartao_id)

    if cartao is None:
        raise ValueError("Cartão não encontrado.")

    if cartao.status != "ATIVO":
        raise ValueError("O cartão está inativo.")

    categoria = buscar_categoria_por_id(categoria_id)

    if categoria is None:
        raise ValueError("Categoria não encontrada.")

    if categoria.status != "ATIVA":
        raise ValueError("A categoria está inativa.")

    if categoria.tipo != "DESPESA":
        raise ValueError(
            "Compras no cartão precisam utilizar uma categoria de DESPESA."
        )

    descricao = descricao.strip()

    if not descricao:
        raise ValueError("A descrição da compra é obrigatória.")

    if valor_total <= 0:
        raise ValueError("O valor da compra deve ser maior que zero.")

    try:
        data_validada = datetime.strptime(
            data_compra,
            "%Y-%m-%d"
        )

        if data_validada.strftime("%Y-%m-%d") != data_compra:
            raise ValueError()

    except ValueError:
        raise ValueError(
            "Informe uma data válida no formato AAAA-MM-DD."
        )

    compra = CompraCartao(
        id=None,
        cartao_id=cartao_id,
        categoria_id=categoria_id,
        descricao=descricao,
        data_compra=data_compra,
        valor_total=valor_total,
        quantidade_parcelas=1,
        observacao=observacao
    )

    mes_referencia = calcular_mes_fatura(
        data_compra,
        cartao.dia_fechamento
    )

    data_fechamento, data_vencimento = calcular_datas_fatura(
        mes_referencia,
        cartao.dia_fechamento,
        cartao.dia_vencimento
    )

    return inserir_compra_com_parcela(
        compra=compra,
        mes_referencia=mes_referencia,
        data_fechamento=data_fechamento,
        data_vencimento=data_vencimento
    )

def localizar_fatura_compra(
    cartao_id: int,
    data_compra: str
):
    cartao = buscar_cartao_por_id(cartao_id)

    if cartao is None:
        raise ValueError("Cartão não encontrado.")

    mes_referencia = calcular_mes_fatura(
        data_compra,
        cartao.dia_fechamento
    )

    fatura = buscar_por_cartao_mes(
        cartao_id,
        mes_referencia
    )

    return mes_referencia, fatura
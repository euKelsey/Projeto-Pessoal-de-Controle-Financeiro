from models.fatura import Fatura
from datetime import datetime
from repositories.fatura_repository import (
    inserir,
    listar,
    buscar_por_id,
    buscar_por_cartao_mes,
    atualizar
)
from repositories.cartao_repository import buscar_por_id as buscar_cartao_por_id

def validar_datas_fatura(
    mes_referencia: str,
    data_fechamento: str,
    data_vencimento: str
):
    try:
        datetime.strptime(
            mes_referencia,
            "%Y-%m"
        )

        fechamento = datetime.strptime(
            data_fechamento,
            "%Y-%m-%d"
        )

        vencimento = datetime.strptime(
            data_vencimento,
            "%Y-%m-%d"
        )

    except ValueError:
        raise ValueError(
            "Informe datas válidas nos formatos AAAA-MM e AAAA-MM-DD."
        )

    if fechamento > vencimento:
        raise ValueError(
            "A data de fechamento não pode ser posterior ao vencimento."
        )

def cadastrar_fatura(
    cartao_id: int,
    mes_referencia: str,
    data_fechamento: str,
    data_vencimento: str
):
    
    validar_datas_fatura(
        mes_referencia,
        data_fechamento,
        data_vencimento
    )
    
    cartao = buscar_cartao_por_id(cartao_id)

    if cartao is None:
        raise ValueError("Cartão não encontrado.")

    fatura_existente = buscar_por_cartao_mes(
        cartao_id,
        mes_referencia
    )

    if fatura_existente is not None:
        raise ValueError(
            "Já existe uma fatura para este cartão neste mês."
        )

    fatura = Fatura(
        id=None,
        cartao_id=cartao_id,
        mes_referencia=mes_referencia,
        data_fechamento=data_fechamento,
        data_vencimento=data_vencimento
    )

    return inserir(fatura)

def listar_faturas():
    return listar()

def buscar_fatura_por_id(fatura_id: int):
    fatura = buscar_por_id(fatura_id)

    if fatura is None:
        raise ValueError("Fatura não encontrada.")

    return fatura

def atualizar_fatura(
    fatura_id: int,
    mes_referencia: str,
    data_fechamento: str,
    data_vencimento: str,
    status: str = "ABERTA"
):
    fatura = buscar_por_id(fatura_id)

    if fatura is None:
        raise ValueError("Fatura não encontrada.")
    
    if fatura.status == "FECHADA":
        raise ValueError(
            "Esta fatura está fechada e não pode ser editada."
        )
    
    validar_datas_fatura(
        mes_referencia,
        data_fechamento,
        data_vencimento
    )

    status = status.strip().upper()

    if status not in ("ABERTA", "FECHADA"):
        raise ValueError(
            "O status da fatura deve ser ABERTA ou FECHADA."
        )

    fatura_existente = buscar_por_cartao_mes(
        fatura.cartao_id,
        mes_referencia
    )

    if (
        fatura_existente is not None
        and fatura_existente.id != fatura_id
    ):
        raise ValueError(
            "Já existe uma fatura para este cartão neste mês."
        )

    fatura.mes_referencia = mes_referencia
    fatura.data_fechamento = data_fechamento
    fatura.data_vencimento = data_vencimento
    fatura.status = status

    return atualizar(fatura)
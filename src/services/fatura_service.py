from models.fatura import Fatura
from datetime import datetime
from datetime import date
from repositories.fatura_repository import (
    inserir,
    listar,
    buscar_por_id,
    buscar_por_cartao_mes,
    calcular_total_fatura,
    fechar_faturas_vencidas,
    processar_faturas_automaticamente,
    atualizar
)
from repositories.fatura_repository import (
    fechar_fatura as fechar_fatura_repository
)
from repositories.cartao_repository import buscar_por_id as buscar_cartao_por_id

from repositories.lancamento_repository import (
    buscar_por_fatura_id
)

from repositories.movimentacao_repository import (
    buscar_por_lancamento_id
)

from services.movimentacao_service import (
    cadastrar_movimentacao
)

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

def obter_total_fatura(fatura_id: int) -> int:
    if not isinstance(fatura_id, int) or fatura_id <= 0:
        raise ValueError("ID da fatura inválido.")

    fatura = buscar_por_id(fatura_id)

    if fatura is None:
        raise ValueError("Fatura não encontrada.")

    return calcular_total_fatura(fatura_id)

def confirmar_fechamento_fatura(fatura_id: int):
    if not isinstance(fatura_id, int) or fatura_id <= 0:
        raise ValueError("ID da fatura inválido.")

    fatura = buscar_por_id(fatura_id)

    if fatura is None:
        raise ValueError("Fatura não encontrada.")

    if fatura.status != "ABERTA":
        raise ValueError("Esta fatura já está fechada.")

    fechou = fechar_fatura_repository(fatura_id)

    if not fechou:
        raise ValueError(
            "Não foi possível fechar a fatura."
        )

    return True

def atualizar_faturas_automaticamente(
    data_referencia: str | None = None
) -> int:
    if data_referencia is None:
        data_referencia = date.today().isoformat()

    quantidade_fechada, quantidade_lancamentos = (
        processar_faturas_automaticamente(data_referencia)
    )

    return quantidade_fechada


def pagar_fatura(
    fatura_id: int,
    data_pagamento: str,
    forma: str,
    observacao: str | None = None
):
    # 1. Validar o ID da fatura.
    if not isinstance(fatura_id, int) or fatura_id <= 0:
        raise ValueError("ID da fatura inválido.")

    # 2. Localizar a fatura.
    fatura = buscar_por_id(fatura_id)

    if fatura is None:
        raise ValueError("Fatura não encontrada.")

    # 3. Verificar se está fechada.
    if fatura.status != "FECHADA":
        raise ValueError(
            "Somente faturas fechadas podem ser pagas."
        )

    # 4. Localizar o lançamento financeiro.
    lancamento = buscar_por_fatura_id(fatura_id)

    if lancamento is None:
        raise ValueError(
            "Esta fatura não possui lançamento financeiro."
        )

    if lancamento.origem != "FATURA":
        raise ValueError(
            "O lançamento não pertence a uma fatura."
        )

    # 5. Verificar se o lançamento está pendente.
    if lancamento.status != "PENDENTE":
        raise ValueError(
            "Esta fatura não possui pagamento pendente."
        )

    # 6. Impedir pagamento duplicado.
    movimentacao_existente = buscar_por_lancamento_id(
        lancamento.id
    )

    if movimentacao_existente is not None:
        raise ValueError(
            "Esta fatura já possui um pagamento registrado."
        )

    # 7. Validar a data informada.
    try:
        data_validada = datetime.strptime(
            data_pagamento, "%Y-%m-%d"
        )

        if data_validada.strftime("%Y-%m-%d") != data_pagamento:
            raise ValueError()

    except ValueError:
        raise ValueError(
            "Informe uma data válida no formato AAAA-MM-DD."
        )

    # 8. Registrar o pagamento integral.
    return cadastrar_movimentacao(
        lancamento_id=lancamento.id,
        valor=lancamento.valor_previsto,
        data_movimentacao=data_pagamento,
        forma=forma,
        observacao=observacao
    )


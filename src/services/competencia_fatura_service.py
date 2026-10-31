
from datetime import date
from calendar import monthrange


def calcular_mes_fatura(
    data_compra: str,
    dia_fechamento: int
) -> str:
    compra = date.fromisoformat(data_compra)

    if not 1 <= dia_fechamento <= 31:
        raise ValueError(
            "O dia de fechamento deve estar entre 1 e 31."
        )

    ultimo_dia = monthrange(
        compra.year,
        compra.month
    )[1]

    fechamento = min(
        dia_fechamento,
        ultimo_dia
    )

    ano = compra.year
    mes = compra.month

    if compra.day >= fechamento:
        if mes == 12:
            ano += 1
            mes = 1
        else:
            mes += 1

    return f"{ano:04d}-{mes:02d}"

def calcular_datas_fatura(
    mes_referencia: str,
    dia_fechamento: int,
    dia_vencimento: int
):
    if not 1 <= dia_fechamento <= 31:
        raise ValueError(
            "Dia de fechamento inválido."
        )

    if not 1 <= dia_vencimento <= 31:
        raise ValueError(
            "Dia de vencimento inválido."
        )

    ano, mes = map(
        int,
        mes_referencia.split("-")
    )

    # Valida o mês e o ano informados.
    date(ano, mes, 1)

    ultimo_dia_fechamento = monthrange(
        ano,
        mes
    )[1]

    dia_real_fechamento = min(
        dia_fechamento,
        ultimo_dia_fechamento
    )

    data_fechamento = date(
        ano,
        mes,
        dia_real_fechamento
    )

    ano_vencimento = ano
    mes_vencimento = mes

    if dia_vencimento <= dia_fechamento:
        if mes_vencimento == 12:
            ano_vencimento += 1
            mes_vencimento = 1
        else:
            mes_vencimento += 1

    ultimo_dia_vencimento = monthrange(
        ano_vencimento,
        mes_vencimento
    )[1]

    dia_real_vencimento = min(
        dia_vencimento,
        ultimo_dia_vencimento
    )

    data_vencimento = date(
        ano_vencimento,
        mes_vencimento,
        dia_real_vencimento
    )

    # Garante que o vencimento seja posterior ao fechamento.
    if data_vencimento <= data_fechamento:
        if mes_vencimento == 12:
            ano_vencimento += 1
            mes_vencimento = 1
        else:
            mes_vencimento += 1

        ultimo_dia_vencimento = monthrange(
            ano_vencimento,
            mes_vencimento
        )[1]

        data_vencimento = date(
            ano_vencimento,
            mes_vencimento,
            min(dia_vencimento, ultimo_dia_vencimento)
        )

    return (
        data_fechamento.isoformat(),
        data_vencimento.isoformat()
    )
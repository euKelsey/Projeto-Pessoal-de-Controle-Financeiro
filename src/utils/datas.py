
from datetime import datetime


def formatar_data_br(valor: str) -> str:
    """
    Recebe uma data digitada e retorna DD/MM/AAAA.
    Aceita DDMMYYYY, DD/MM/YYYY ou YYYY-MM-DD.
    """

    valor = valor.strip()

    if "-" in valor:
        data = datetime.strptime(valor, "%Y-%m-%d")

    elif "/" in valor:
        data = datetime.strptime(valor, "%d/%m/%Y")

    else:
        if len(valor) != 8 or not valor.isdigit():
            raise ValueError("Informe a data com 8 dígitos.")

        data = datetime.strptime(valor, "%d%m%Y")

    return data.strftime("%d/%m/%Y")


def data_para_banco(valor: str) -> str:
    """
    Converte a data para o formato YYYY-MM-DD,
    utilizado pelo SQLite.
    """

    data_formatada = formatar_data_br(valor)

    data = datetime.strptime(
        data_formatada,
        "%d/%m/%Y"
    )

    return data.strftime("%Y-%m-%d")

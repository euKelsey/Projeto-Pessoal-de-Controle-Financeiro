
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


def vincular_formatacao_data(campo):
    """Formata automaticamente uma data brasileira ao sair de um CTkEntry.

    Valores incompletos/invalidos permanecem para a validacao ao salvar.
    """
    def ao_sair(event=None):
        texto = campo.get().strip()
        if not texto:
            return
        try:
            data_formatada = formatar_data_br(texto)
        except (ValueError, TypeError):
            return
        if data_formatada != texto:
            campo.delete(0, "end")
            campo.insert(0, data_formatada)

    campo.bind("<FocusOut>", ao_sair)

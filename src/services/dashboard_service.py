from datetime import datetime, date, timedelta

from repositories.dashboard_repository import (
    obter_resumo_mensal,
    listar_proximos_vencimentos,
    listar_resumo_faturas,
    obter_total_compras_cartao,
    obter_total_despesas_comuns
)

def consultar_resumo_mensal(mes_referencia: str) -> dict:
    # Validar o mês informado.
    try:
        data = datetime.strptime(
            mes_referencia,
            "%Y-%m"
        )

        if data.strftime("%Y-%m") != mes_referencia:
            raise ValueError()

    except ValueError:
        raise ValueError(
            "Informe um mês válido no formato AAAA-MM."
        )

    # Consultar os dados financeiros.
    resumo = obter_resumo_mensal(mes_referencia)

    # Calcular o saldo realizado por competência prevista.
    resumo["saldo_realizado"] = (
        resumo["recebido"] - resumo["pago"]
    )

    return resumo


def consultar_proximos_vencimentos(
    quantidade: int = 10
) -> list:

    # Obter a data atual
    hoje = date.today()

    # Definir o período dos próximos 30 dias
    data_limite = hoje + timedelta(days=30)

    # Buscar vencimentos pendentes no banco
    vencimentos = listar_proximos_vencimentos(
        data_limite=data_limite.isoformat(),
        quantidade=quantidade
    )

    # Identificar as contas atrasadas
    for vencimento in vencimentos:
        data_vencimento = date.fromisoformat(
            vencimento["data_vencimento"]
        )

        if data_vencimento < hoje:
            vencimento["situacao"] = "ATRASADA"

        elif data_vencimento == hoje:
            vencimento["situacao"] = "VENCE HOJE"

        else:
            vencimento["situacao"] = "PENDENTE"

        vencimento["dias_restantes"] = (
            data_vencimento - hoje
        ).days

    return vencimentos


def consultar_resumo_faturas(
    quantidade: int = 6
) -> list:

    if not isinstance(quantidade, int) or quantidade <= 0:
        raise ValueError(
            "A quantidade deve ser um número inteiro positivo."
        )

    faturas = listar_resumo_faturas(
        quantidade=quantidade
    )

    for fatura in faturas:

        if fatura["status"] == "ABERTA":
            fatura["situacao"] = "ABERTA"

        elif fatura["status_lancamento"] == "PENDENTE":
            fatura["situacao"] = "AGUARDANDO PAGAMENTO"

        elif fatura["status_lancamento"] == "EFETIVADO":
            fatura["situacao"] = "PAGA"

        else:
            fatura["situacao"] = "FECHADA"

    return faturas


def consultar_gastos_mensais(mes_referencia: str) -> dict:

    # Validar o formato do mês
    try:
        data_mes = datetime.strptime(
            mes_referencia,
            "%Y-%m"
        )

        if data_mes.strftime("%Y-%m") != mes_referencia:
            raise ValueError

    except (ValueError, TypeError):
        raise ValueError(
            "O mês deve estar no formato AAAA-MM."
        )

    # Consultar despesas comuns
    despesas_comuns = obter_total_despesas_comuns(
        mes_referencia
    )

    # Consultar compras realizadas no cartão
    compras_cartao = obter_total_compras_cartao(
        mes_referencia
    )

    # Somar os gastos do mês sem duplicar faturas
    total_gasto = despesas_comuns + compras_cartao

    return {
        "mes_referencia": mes_referencia,
        "despesas_comuns": despesas_comuns,
        "compras_cartao": compras_cartao,
        "total_gasto": total_gasto
    }


from dataclasses import dataclass


@dataclass
class Fatura:
    id: int | None
    cartao_id: int
    mes_referencia: str
    data_fechamento: str
    data_vencimento: str
    status: str = "ABERTA"
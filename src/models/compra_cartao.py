
from dataclasses import dataclass


@dataclass
class CompraCartao:
    id: int | None
    cartao_id: int
    categoria_id: int
    descricao: str
    data_compra: str
    valor_total: int
    quantidade_parcelas: int
    recorrencia_id: int | None = None
    primeira_parcela_controlada: int = 0
    data_primeira_parcela_controlada: str | None = None
    status: str = "ATIVA"
    observacao: str | None = None

from dataclasses import dataclass


@dataclass
class Cartao:
    id: int | None
    nome: str
    instituicao: str
    limite_total: int
    dia_fechamento: int
    dia_vencimento: int
    status: str = "ATIVO"
    observacao: str | None = None
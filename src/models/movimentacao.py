from dataclasses import dataclass


@dataclass
class Movimentacao:
    id: int | None
    lancamento_id: int
    valor: int
    data_movimentacao: str
    forma: str
    observacao: str | None = None
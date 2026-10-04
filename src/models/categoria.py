from dataclasses import dataclass


@dataclass
class Categoria:
    id: int | None
    nome: str
    tipo: str
    descricao: str | None = None
    status: str = "ATIVA"
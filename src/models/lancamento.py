from dataclasses import dataclass 

@dataclass 
class Lancamento:
    id: int | None 
    tipo: str 
    descricao: str 
    valor_previsto: int 
    data_prevista: str 
    categoria_id: int | None 
    recorrencia_id: int | None = None 
    fatura_id: int | None = None 
    status: str = "PENDENTE"
    observacao: str | None = None 
    origem: str = "MANUAL"
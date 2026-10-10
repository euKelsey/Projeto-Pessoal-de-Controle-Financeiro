from database.conexao import inicializar_banco
from services.lancamento_service import atualizar_lancamento


inicializar_banco()

lancamento = atualizar_lancamento(
    lancamento_id=1,
    tipo="despesa",
    descricao="Conta de luz atualizada",
    valor_previsto=22000,
    data_prevista="2026-10-18",
    categoria_id=1,
    status="pendente",
    observacao="Valor e data atualizados"
)

print(lancamento)
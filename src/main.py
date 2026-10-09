from database.conexao import inicializar_banco
from repositories.cartao_repository import buscar_por_id, atualizar


inicializar_banco()

cartao = buscar_por_id(1)

cartao.limite_total = 600000
cartao.observacao = "Limite atualizado"
cartao.status = "ATIVO"
atualizar(cartao)

cartao_atualizado = atualizar(cartao)

print(cartao_atualizado)
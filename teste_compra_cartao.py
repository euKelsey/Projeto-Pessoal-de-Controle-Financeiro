import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parent / "src")
)

from services.compra_cartao_service import cadastrar_compra
from services.cartao_service import listar_cartoes
from services.categoria_service import listar_categorias_ativas


cartao = next(
    (c for c in listar_cartoes() if c.status == "ATIVO"),
    None
)

categoria = next(
    (
        c for c in listar_categorias_ativas()
        if c.tipo == "DESPESA"
    ),
    None
)

if cartao is None or categoria is None:
    print("É necessário ter um cartão e uma categoria de despesa ativos.")

else:
    compra = cadastrar_compra(
        cartao_id=cartao.id,
        categoria_id=categoria.id,
        descricao="TESTE V1 COMPRA 1X",
        data_compra="2026-10-31",
        valor_total=25990,
        observacao="Teste da V1"
    )

    print(compra)
    print("Quantidade de parcelas:", compra.quantidade_parcelas)
    print("ID da compra salva:", compra.id)
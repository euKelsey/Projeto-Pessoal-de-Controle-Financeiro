from database.conexao import conectar
from models.compra_cartao import CompraCartao
def inserir(compra: CompraCartao):
    conexao = conectar()

    try:
        cursor = conexao.cursor()

        cursor.execute("""
            INSERT INTO compra_cartao (
                cartao_id,
                categoria_id,
                recorrencia_id,
                descricao,
                data_compra,
                valor_total,
                quantidade_parcelas,
                primeira_parcela_controlada,
                data_primeira_parcela_controlada,
                status,
                observacao
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, (
            compra.cartao_id,
            compra.categoria_id,
            compra.recorrencia_id,
            compra.descricao,
            compra.data_compra,
            compra.valor_total,
            compra.quantidade_parcelas,
            compra.primeira_parcela_controlada,
            compra.data_primeira_parcela_controlada,
            compra.status,
            compra.observacao
        ))

        conexao.commit()

        compra.id = cursor.lastrowid

        return compra

    except Exception:
        conexao.rollback()
        raise

    finally:
        conexao.close()
        
def listar():
    conexao = conectar()

    try:
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT
                id,
                cartao_id,
                categoria_id,
                descricao,
                data_compra,
                valor_total,
                quantidade_parcelas,
                recorrencia_id,
                primeira_parcela_controlada,
                data_primeira_parcela_controlada,
                status,
                observacao
            FROM compra_cartao
            ORDER BY data_compra DESC, id DESC;
        """)

        registros = cursor.fetchall()
        compras = []

        for registro in registros:
            compra = CompraCartao(
                id=registro[0],
                cartao_id=registro[1],
                categoria_id=registro[2],
                descricao=registro[3],
                data_compra=registro[4],
                valor_total=registro[5],
                quantidade_parcelas=registro[6],
                recorrencia_id=registro[7],
                primeira_parcela_controlada=registro[8],
                data_primeira_parcela_controlada=registro[9],
                status=registro[10],
                observacao=registro[11]
            )

            compras.append(compra)

        return compras

    finally:
        conexao.close()
        
def buscar_por_id(compra_id: int):
    conexao = conectar()

    try:
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT
                id,
                cartao_id,
                categoria_id,
                descricao,
                data_compra,
                valor_total,
                quantidade_parcelas,
                recorrencia_id,
                primeira_parcela_controlada,
                data_primeira_parcela_controlada,
                status,
                observacao
            FROM compra_cartao
            WHERE id = ?;
        """, (compra_id,))

        registro = cursor.fetchone()

        if registro is None:
            return None

        return CompraCartao(
            id=registro[0],
            cartao_id=registro[1],
            categoria_id=registro[2],
            descricao=registro[3],
            data_compra=registro[4],
            valor_total=registro[5],
            quantidade_parcelas=registro[6],
            recorrencia_id=registro[7],
            primeira_parcela_controlada=registro[8],
            data_primeira_parcela_controlada=registro[9],
            status=registro[10],
            observacao=registro[11]
        )

    finally:
        conexao.close()


def inserir_compra_com_parcela(
    compra: CompraCartao,
    mes_referencia: str,
    data_fechamento: str,
    data_vencimento: str
):
    conexao = conectar()

    try:
        cursor = conexao.cursor()
        
        cursor.execute("""
            SELECT id, status
            FROM fatura
            WHERE cartao_id = ?
              AND mes_referencia = ?;
        """, (
            compra.cartao_id,
            mes_referencia
        ))

        registro_fatura = cursor.fetchone()

        if registro_fatura is not None:
            fatura_id = registro_fatura[0]
            status_fatura = registro_fatura[1]

            if status_fatura != "ABERTA":
                raise ValueError(
                    "A fatura correspondente está fechada."
                )

        else:
            cursor.execute("""
                INSERT INTO fatura (
                    cartao_id,
                    mes_referencia,
                    data_fechamento,
                    data_vencimento,
                    status
                )
                VALUES (?, ?, ?, ?, 'ABERTA');
            """, (
                compra.cartao_id,
                mes_referencia,
                data_fechamento,
                data_vencimento
            ))

            fatura_id = cursor.lastrowid

        cursor.execute("""
            INSERT INTO compra_cartao (
                cartao_id,
                categoria_id,
                recorrencia_id,
                descricao,
                data_compra,
                valor_total,
                quantidade_parcelas,
                primeira_parcela_controlada,
                data_primeira_parcela_controlada,
                status,
                observacao
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, (
            compra.cartao_id,
            compra.categoria_id,
            compra.recorrencia_id,
            compra.descricao,
            compra.data_compra,
            compra.valor_total,
            compra.quantidade_parcelas,
            compra.primeira_parcela_controlada,
            compra.data_primeira_parcela_controlada,
            compra.status,
            compra.observacao
        ))

        compra_id = cursor.lastrowid

        cursor.execute("""
            INSERT INTO parcela_cartao (
                compra_cartao_id,
                fatura_id,
                numero_parcela,
                valor,
                data_prevista
            )
            VALUES (?, ?, ?, ?, ?);
        """, (
            compra_id,
            fatura_id,
            1,
            compra.valor_total,
            data_vencimento
        ))
        
        conexao.commit()

        compra.id = compra_id

        return compra

    except Exception:
        conexao.rollback()
        raise

    finally:
        conexao.close()

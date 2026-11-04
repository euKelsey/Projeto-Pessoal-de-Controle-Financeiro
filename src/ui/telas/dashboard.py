
import customtkinter as ctk
from datetime import date

from services.dashboard_service import (
    consultar_resumo_mensal,
    consultar_proximos_vencimentos,
    consultar_resumo_faturas,
    consultar_gastos_mensais
)


# ============================================
# PADRÃO VISUAL DO DASHBOARD - V1.0
# ============================================

# Cores
COR_FUNDO = "#242424"
COR_CARD = "#303030"
COR_BORDA = "#404040"

COR_TEXTO = "#FFFFFF"
COR_TEXTO_SECUNDARIO = "#B0B0B0"

COR_RECEITA = "#35C48A"
COR_DESPESA = "#F07878"
COR_ALERTA = "#FFA500"
COR_DESTAQUE = "#2474A6"

# Fontes
FONTE_TITULO = 24
FONTE_SECAO = 18
FONTE_INDICADOR = 22
FONTE_TEXTO = 14
FONTE_AUXILIAR = 12

# Espaçamentos
ESPACAMENTO_SECAO = 15
ESPACAMENTO_INTERNO = 15

# Aparência dos cartões
RAIO_CARD = 10


class TelaDashboard(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        # Área principal com rolagem
        self.conteudo = ctk.CTkScrollableFrame(self)

        self.conteudo.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        # Título principal
        self.titulo = ctk.CTkLabel(
            self.conteudo,
            text="Visão Financeira",
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        )

        self.titulo.pack(
            anchor="w",
            padx=10,
            pady=(10, 5)
        )
        

        self.frame_acoes = ctk.CTkFrame(
            self.conteudo,
            fg_color="transparent"
        )

        self.frame_acoes.pack(
            fill="x",
            padx=10,
            pady=(5, 15)
        )

        self.botao_nova_compra = ctk.CTkButton(
            self.frame_acoes,
            text="+ Nova Compra",
            width=150,
            command=self.abrir_nova_compra
        )

        self.botao_nova_compra.pack(
            side="left",
            padx=(0, 10)
        )


        self.botao_nova_receita = ctk.CTkButton(
            self.frame_acoes,
            text="+ Nova Receita",
            width=150,
            command=lambda: self.abrir_novo_lancamento(
                "RECEITA"
            )
        )

        self.botao_nova_receita.pack(
            side="left",
            padx=(0, 10)
        )

        self.botao_nova_despesa = ctk.CTkButton(
            self.frame_acoes,
            text="+ Nova Despesa",
            width=150,
            command=lambda: self.abrir_novo_lancamento(
                "DESPESA"
            )
        )

        self.botao_nova_despesa.pack(
            side="left",
            padx=(0, 10)
        )


        # Mês atual
        mes_atual = date.today().strftime("%m/%Y")
        
        # Consultar os dados do mês atual
        mes_referencia = date.today().strftime("%Y-%m")

        resumo = consultar_resumo_mensal(mes_referencia)
        
        
        # Consultar os gastos do mês atual
        gastos = consultar_gastos_mensais(
            mes_referencia
        )

        # Atualizar as despesas considerando
        # compras no cartão, mesmo com fatura aberta
        resumo["despesas"] = gastos["total_gasto"]

        # Recalcular o saldo considerando os gastos
        resumo["saldo_previsto"] = (
            resumo["receitas"] - gastos["total_gasto"]
        )


        self.label_mes = ctk.CTkLabel(
            self.conteudo,
            text=f"Resumo financeiro - {mes_atual}",
            font=ctk.CTkFont(size=15)
        )

        self.label_mes.pack(
            anchor="w",
            padx=10,
            pady=(0, 20)
        )

        # Área dos indicadores financeiros
        self.frame_indicadores = ctk.CTkFrame(
            self.conteudo
        )

        self.frame_indicadores.pack(
            fill="x",
            padx=10,
            pady=10
        )
        

        # Configurar duas colunas de indicadores
        self.frame_indicadores.grid_columnconfigure(
            (0, 1),
            weight=1
        )

        indicadores = [
            ("Receitas do mês", resumo["receitas"]),
            ("Gastos do mês (inclui cartão)", resumo["despesas"]),
            ("Receitas recebidas", resumo["recebido"]),
            ("Contas quitadas", resumo["pago"]),
            ("Receitas pendentes", resumo["a_receber"]),
            ("Contas pendentes", resumo["a_pagar"])
        ]

        for indice, (titulo, valor) in enumerate(indicadores):
            linha = indice // 2
            coluna = indice % 2

            cartao = ctk.CTkFrame(
                self.frame_indicadores,
                corner_radius=10
            )

            cartao.grid(
                row=linha,
                column=coluna,
                padx=10,
                pady=10,
                sticky="ew"
            )

            label_titulo = ctk.CTkLabel(
                cartao,
                text=titulo,
                font=ctk.CTkFont(size=14)
            )

            label_titulo.pack(
                padx=15,
                pady=(15, 5),
                anchor="w"
            )

            valor_formatado = (
                f"R$ {valor / 100:,.2f}"
                .replace(",", "X")
                .replace(".", ",")
                .replace("X", ".")
            )

            label_valor = ctk.CTkLabel(
                cartao,
                text=valor_formatado,
                font=ctk.CTkFont(
                    size=23,
                    weight="bold"
                )
            )

            label_valor.pack(
                padx=15,
                pady=(0, 15),
                anchor="w"
            )
            


        # Padronizar os seis indicadores financeiros
        for cartao in self.frame_indicadores.winfo_children():

            if not isinstance(cartao, ctk.CTkFrame):
                continue

            # Aparência do cartão
            cartao.configure(
                fg_color=COR_CARD,
                corner_radius=RAIO_CARD,
                border_width=1,
                border_color=COR_BORDA
            )

            # Localizar os textos do cartão
            labels = [
                widget
                for widget in cartao.winfo_children()
                if isinstance(widget, ctk.CTkLabel)
            ]

            # Padronizar título e valor
            if len(labels) == 2:

                label_titulo = labels[0]
                label_valor = labels[1]

                label_titulo.configure(
                    font=ctk.CTkFont(
                        size=FONTE_AUXILIAR,
                        weight="normal"
                    ),
                    text_color=COR_TEXTO_SECUNDARIO,
                    anchor="w"
                )

                label_valor.configure(
                    font=ctk.CTkFont(
                        size=FONTE_INDICADOR,
                        weight="bold"
                    ),
                    anchor="w"
                )

                # Destacar receitas e gastos
                titulo_indicador = label_titulo.cget("text")

                if titulo_indicador == "Receitas do mês":
                    label_valor.configure(
                        text_color=COR_RECEITA
                    )

                elif titulo_indicador.startswith("Gastos do mês"):
                    label_valor.configure(
                        text_color=COR_DESPESA
                    )

                else:
                    label_valor.configure(
                        text_color=COR_TEXTO
                    )

        # Saldo previsto do mês
        saldo = resumo["saldo_previsto"]

        saldo_formatado = (
            f"R$ {saldo / 100:,.2f}"
            .replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )

        cor_saldo = (
            "#2ECC71" if saldo >= 0 else "#FF6B6B"
        )

        self.frame_saldo = ctk.CTkFrame(
            self.conteudo,
            corner_radius=10
        )

        self.frame_saldo.pack(
            fill="x",
            padx=10,
            pady=10
        )

        ctk.CTkLabel(
            self.frame_saldo,
            text="Saldo previsto do mês",
            font=ctk.CTkFont(size=16)
        ).pack(
            padx=15,
            pady=(15, 5),
            anchor="w"
        )

        ctk.CTkLabel(
            self.frame_saldo,
            text=saldo_formatado,
            text_color=cor_saldo,
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        ).pack(
            padx=15,
            pady=(0, 15),
            anchor="w"
        )


        # ============================================
        # PADRONIZAÇÃO DO CARTÃO DE SALDO
        # ============================================

        self.frame_saldo.configure(
            fg_color=COR_CARD,
            corner_radius=RAIO_CARD,
            border_width=1,
            border_color=COR_BORDA
        )

        # Reduzir o espaço externo do cartão
        self.frame_saldo.pack_configure(
            fill="x",
            padx=10,
            pady=(5, 10)
        )

        # Padronizar os textos do saldo
        for widget in self.frame_saldo.winfo_children():

            if not isinstance(widget, ctk.CTkLabel):
                continue

            texto = widget.cget("text")

            if "R$" in texto:
                widget.configure(
                    font=ctk.CTkFont(
                        size=28,
                        weight="bold"
                    ),
                    anchor="w"
                )

            else:
                widget.configure(
                    text="Saldo após gastos",
                    font=ctk.CTkFont(
                        size=FONTE_TEXTO,
                        weight="normal"
                    ),
                    text_color=COR_TEXTO_SECUNDARIO,
                    anchor="w"
                )

            widget.pack_configure(
                padx=15,
                pady=5
            )


        # Área dos próximos vencimentos
        self.frame_vencimentos = ctk.CTkFrame(
            self.conteudo
        )
        

        # Informação sobre os indicadores financeiros
        aviso_indicadores = ctk.CTkLabel(
            self.conteudo,
            text=(
                "Gastos do mês incluem compras no cartão, "
                "mesmo com fatura aberta. "
                "Recebimentos, pagamentos e pendências "
                "são apresentados conforme o mês "
                "de vencimento dos lançamentos."
            ),
            font=ctk.CTkFont(size=12),
            text_color="gray70",
            wraplength=650,
            justify="left"
        )

        aviso_indicadores.pack(
            fill="x",
            padx=20,
            pady=(5, 15)
        )


        self.frame_vencimentos.pack(
            fill="x",
            padx=10,
            pady=10
        )
        

        # Título da seção de vencimentos
        titulo_vencimentos = ctk.CTkLabel(
            self.frame_vencimentos,
            text="Contas a Pagar - Próximos Vencimentos",
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            )
        )

        titulo_vencimentos.pack(
            anchor="w",
            padx=15,
            pady=(15, 10)
        )

        # Consultar despesas pendentes
        vencimentos = consultar_proximos_vencimentos()

        if not vencimentos:
            mensagem = ctk.CTkLabel(
                self.frame_vencimentos,
                text="Nenhuma conta pendente encontrada."
            )

            mensagem.pack(
                padx=15,
                pady=15
            )


        for vencimento in vencimentos:

            # Criar cartão individual
            linha = ctk.CTkFrame(
                self.frame_vencimentos,
                fg_color=COR_CARD,
                corner_radius=RAIO_CARD,
                border_width=1,
                border_color=COR_BORDA
            )

            linha.pack(
                fill="x",
                padx=15,
                pady=5
            )

            # Área esquerda: descrição e vencimento
            frame_info = ctk.CTkFrame(
                linha,
                fg_color="transparent"
            )

            frame_info.pack(
                side="left",
                fill="both",
                expand=True,
                padx=15,
                pady=10
            )

            label_descricao = ctk.CTkLabel(
                frame_info,
                text=vencimento["descricao"],
                font=ctk.CTkFont(
                    size=FONTE_TEXTO,
                    weight="bold"
                ),
                text_color=COR_TEXTO,
                anchor="w"
            )

            label_descricao.pack(
                fill="x"
            )

            # Formatar data para DD/MM/AAAA
            data_original = vencimento["data_vencimento"]

            ano, mes, dia = data_original.split("-")

            data_formatada = f"{dia}/{mes}/{ano}"

            label_data = ctk.CTkLabel(
                frame_info,
                text=f"Vencimento: {data_formatada}",
                font=ctk.CTkFont(
                    size=FONTE_AUXILIAR
                ),
                text_color=COR_TEXTO_SECUNDARIO,
                anchor="w"
            )

            label_data.pack(
                fill="x"
            )

            # Área direita: valor e situação
            frame_valores = ctk.CTkFrame(
                linha,
                fg_color="transparent"
            )

            frame_valores.pack(
                side="right",
                padx=15,
                pady=10
            )

            valor = vencimento["valor"]

            valor_formatado = (
                f"R$ {valor / 100:,.2f}"
                .replace(",", "X")
                .replace(".", ",")
                .replace("X", ".")
            )

            label_valor = ctk.CTkLabel(
                frame_valores,
                text=valor_formatado,
                font=ctk.CTkFont(
                    size=FONTE_TEXTO,
                    weight="bold"
                ),
                text_color=COR_TEXTO
            )

            label_valor.pack(
                anchor="e"
            )

            # Definir a cor da situação
            situacao = vencimento["situacao"]

            if situacao == "ATRASADA":
                cor_situacao = COR_DESPESA

            elif situacao == "VENCE HOJE":
                cor_situacao = COR_ALERTA

            else:
                cor_situacao = COR_RECEITA

            label_situacao = ctk.CTkLabel(
                frame_valores,
                text=situacao,
                font=ctk.CTkFont(
                    size=FONTE_AUXILIAR,
                    weight="bold"
                ),
                text_color=cor_situacao
            )

            label_situacao.pack(
                anchor="e"
            )



        # Área de cartões
        self.frame_cartoes = ctk.CTkFrame(
            self.conteudo
        )
        


        # ============================================
        # COMPOSIÇÃO DOS GASTOS DO MÊS
        # ============================================

        frame_detalhamento = ctk.CTkFrame(
            self.conteudo,
            fg_color=COR_FUNDO,
            corner_radius=RAIO_CARD
        )

        frame_detalhamento.pack(
            fill="x",
            padx=10,
            pady=(5, 10)
        )

        titulo_detalhamento = ctk.CTkLabel(
            frame_detalhamento,
            text="Composição dos Gastos do Mês",
            font=ctk.CTkFont(
                size=FONTE_SECAO,
                weight="bold"
            ),
            text_color=COR_TEXTO
        )

        titulo_detalhamento.pack(
            anchor="w",
            padx=15,
            pady=(10, 10)
        )

        # Cartão interno com os valores
        frame_valores_gastos = ctk.CTkFrame(
            frame_detalhamento,
            fg_color=COR_CARD,
            corner_radius=RAIO_CARD,
            border_width=1,
            border_color=COR_BORDA
        )

        frame_valores_gastos.pack(
            fill="x",
            padx=15,
            pady=(0, 10)
        )

        # Formatar valores em reais
        def formatar_reais(valor):
            return (
                f"R$ {valor / 100:,.2f}"
                .replace(",", "X")
                .replace(".", ",")
                .replace("X", ".")
            )

        # Informações que serão exibidas
        linhas_gastos = [
            (
                "Despesas comuns",
                gastos["despesas_comuns"],
                COR_TEXTO
            ),
            (
                "Compras no cartão",
                gastos["compras_cartao"],
                COR_TEXTO
            ),
            (
                "Total gasto",
                gastos["total_gasto"],
                COR_DESPESA
            )
        ]

        for indice, (descricao, valor, cor) in enumerate(
            linhas_gastos
        ):
            linha = ctk.CTkFrame(
                frame_valores_gastos,
                fg_color="transparent"
            )

            linha.pack(
                fill="x",
                padx=15,
                pady=10
            )

            label_descricao = ctk.CTkLabel(
                linha,
                text=descricao,
                font=ctk.CTkFont(
                    size=FONTE_TEXTO,
                    weight="bold" if indice == 2 else "normal"
                ),
                text_color=COR_TEXTO_SECUNDARIO,
                anchor="w"
            )

            label_descricao.pack(
                side="left",
                fill="x",
                expand=True
            )

            label_valor = ctk.CTkLabel(
                linha,
                text=formatar_reais(valor),
                font=ctk.CTkFont(
                    size=FONTE_INDICADOR if indice == 2
                    else FONTE_TEXTO,
                    weight="bold"
                ),
                text_color=cor
            )

            label_valor.pack(
                side="right"
            )

            # Separar as linhas visualmente
            if indice < 2:
                separador = ctk.CTkFrame(
                    frame_valores_gastos,
                    height=1,
                    fg_color=COR_BORDA
                )

                separador.pack(
                    fill="x",
                    padx=15
                )

        self.frame_cartoes.pack(
            fill="x",
            padx=10,
            pady=10
        )
        

        # Título da seção de cartões
        titulo_cartoes = ctk.CTkLabel(
            self.frame_cartoes,
            text="Cartões de Crédito - Faturas",
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            )
        )

        titulo_cartoes.pack(
            anchor="w",
            padx=15,
            pady=(15, 10)
        )

        # Consultar faturas no banco
        faturas = consultar_resumo_faturas()

        if not faturas:
            mensagem = ctk.CTkLabel(
                self.frame_cartoes,
                text="Nenhuma fatura pendente encontrada."
            )

            mensagem.pack(
                padx=15,
                pady=15
            )

        for fatura in faturas:

            # Cartão individual da fatura
            linha = ctk.CTkFrame(
                self.frame_cartoes,
                fg_color=COR_CARD,
                corner_radius=RAIO_CARD,
                border_width=1,
                border_color=COR_BORDA
            )

            linha.pack(
                fill="x",
                padx=15,
                pady=6
            )

            # Cabeçalho: cartão e situação
            cabecalho = ctk.CTkFrame(
                linha,
                fg_color="transparent"
            )

            cabecalho.pack(
                fill="x",
                padx=15,
                pady=(12, 5)
            )

            label_cartao = ctk.CTkLabel(
                cabecalho,
                text=fatura["cartao"],
                font=ctk.CTkFont(
                    size=FONTE_SECAO,
                    weight="bold"
                ),
                text_color=COR_TEXTO
            )

            label_cartao.pack(side="left")

            situacao = fatura["situacao"]

            if situacao == "ABERTA":
                cor_situacao = COR_RECEITA

            elif situacao == "AGUARDANDO PAGAMENTO":
                cor_situacao = COR_ALERTA

            else:
                cor_situacao = COR_TEXTO_SECUNDARIO

            label_situacao = ctk.CTkLabel(
                cabecalho,
                text=situacao,
                font=ctk.CTkFont(
                    size=FONTE_AUXILIAR,
                    weight="bold"
                ),
                text_color=cor_situacao
            )

            label_situacao.pack(side="right")

            # Valor da fatura
            valor = fatura["total"]

            valor_formatado = (
                f"R$ {valor / 100:,.2f}"
                .replace(",", "X")
                .replace(".", ",")
                .replace("X", ".")
            )

            label_valor = ctk.CTkLabel(
                linha,
                text=valor_formatado,
                font=ctk.CTkFont(
                    size=FONTE_INDICADOR,
                    weight="bold"
                ),
                text_color=COR_TEXTO
            )

            label_valor.pack(
                anchor="w",
                padx=15,
                pady=(0, 10)
            )

            # Separador
            separador = ctk.CTkFrame(
                linha,
                height=1,
                fg_color=COR_BORDA
            )

            separador.pack(
                fill="x",
                padx=15,
                pady=(0, 5)
            )

            # Mês de referência
            ano, mes = fatura["mes_referencia"].split("-")

            mes_formatado = f"{mes}/{ano}"

            label_mes = ctk.CTkLabel(
                linha,
                text=f"Mês de referência: {mes_formatado}",
                font=ctk.CTkFont(
                    size=FONTE_TEXTO
                ),
                text_color=COR_TEXTO_SECUNDARIO,
                anchor="w"
            )

            label_mes.pack(
                fill="x",
                padx=15,
                pady=3
            )

            # Data de vencimento
            ano, mes, dia = fatura["vencimento"].split("-")

            vencimento_formatado = f"{dia}/{mes}/{ano}"

            label_vencimento = ctk.CTkLabel(
                linha,
                text=f"Vencimento: {vencimento_formatado}",
                font=ctk.CTkFont(
                    size=FONTE_TEXTO
                ),
                text_color=COR_TEXTO_SECUNDARIO,
                anchor="w"
            )

            label_vencimento.pack(
                fill="x",
                padx=15,
                pady=(3, 12)
            )
            

        # ============================================
        # PADRONIZAÇÃO GERAL DAS SEÇÕES
        # ============================================

        secoes = [
            self.frame_vencimentos,
            self.frame_cartoes
        ]

        for secao in secoes:

            # Uniformizar o fundo das seções
            secao.configure(
                fg_color=COR_FUNDO,
                corner_radius=RAIO_CARD,
                border_width=0
            )

            # Uniformizar o espaço externo
            secao.pack_configure(
                fill="x",
                padx=10,
                pady=(5, 10)
            )

            # Localizar o título principal da seção
            for widget in secao.winfo_children():

                if isinstance(widget, ctk.CTkLabel):

                    texto = widget.cget("text")

                    if texto.startswith((
                        "Contas a Pagar",
                        "Cartões de Crédito"
                    )):
                        widget.configure(
                            font=ctk.CTkFont(
                                size=FONTE_SECAO,
                                weight="bold"
                            ),
                            text_color=COR_TEXTO,
                            anchor="w"
                        )

    def abrir_nova_compra(self):
        aplicativo = self.winfo_toplevel()
        aplicativo.abrir_nova_compra()


    def abrir_novo_lancamento(self, tipo):
        aplicativo = self.winfo_toplevel()

        aplicativo.abrir_novo_lancamento(
            tipo
        )




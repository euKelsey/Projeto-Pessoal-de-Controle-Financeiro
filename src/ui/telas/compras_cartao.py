import customtkinter as ctk
from datetime import date

from services.cartao_service import listar_cartoes

from services.categoria_service import (
    listar_categorias_ativas,
    listar_categorias
)

from decimal import Decimal, InvalidOperation
from tkinter import messagebox

from services.compra_cartao_service import (
    cadastrar_compra,
    listar_compras
)

class TelaComprasCartao(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.titulo = ctk.CTkLabel(
            self,
            text="Compras no Cartão",
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        )

        self.titulo.pack(
            padx=30,
            pady=(30, 20),
            anchor="nw"
        )

        self.botao_nova_compra = ctk.CTkButton(
            self,
            text="Nova Compra",
            command=self.abrir_formulario_compra
        )

        self.botao_nova_compra.pack(
            padx=30,
            pady=(0, 20),
            anchor="nw"
        )

        self.lista_compras = ctk.CTkScrollableFrame(
            self
        )

        self.lista_compras.pack(
            padx=30,
            pady=(0, 30),
            fill="both",
            expand=True
        )
        
        self.carregar_compras()

    def carregar_compras(self):
        # Limpar a listagem atual
        for widget in self.lista_compras.winfo_children():
            widget.destroy()

        # Consultar dados do banco
        compras = listar_compras()
        cartoes = listar_cartoes()
        categorias = listar_categorias()

        # Relacionar os IDs aos nomes
        nomes_cartoes = {
            cartao.id: cartao.nome
            for cartao in cartoes
        }

        nomes_categorias = {
            categoria.id: categoria.nome
            for categoria in categorias
        }

        # Exibir as compras
        for compra in compras:
            linha = ctk.CTkFrame(
                self.lista_compras
            )

            linha.pack(
                padx=10,
                pady=8,
                fill="x"
            )

            nome_cartao = nomes_cartoes.get(
                compra.cartao_id,
                "Cartão não encontrado"
            )

            nome_categoria = nomes_categorias.get(
                compra.categoria_id,
                "Categoria não encontrada"
            )

            valor_formatado = (
                f"R$ {compra.valor_total / 100:,.2f}"
                .replace(",", "X")
                .replace(".", ",")
                .replace("X", ".")
            )

            texto = (
                f"{compra.descricao} | "
                f"{nome_cartao} | "
                f"{nome_categoria} | "
                f"{valor_formatado} | "
                f"Data: {compra.data_compra} | "
                f"1x | "
                f"{compra.status}"
            )

            label = ctk.CTkLabel(
                linha,
                text=texto,
                anchor="w"
            )

            label.pack(
                padx=10,
                pady=10,
                fill="x"
            )

    def abrir_formulario_compra(self):
        janela = ctk.CTkToplevel(self)

        janela.title("Nova Compra no Cartão")
        janela.geometry("480x700")

        janela.transient(self)
        janela.grab_set()
        janela.focus_force()

        titulo = ctk.CTkLabel(
            janela,
            text="Cadastrar Compra",
            font=ctk.CTkFont(
                size=22,
                weight="bold"
            )
        )

        titulo.pack(pady=(25, 20))
        

        # Buscar cartoes ativos
        cartoes = [
            cartao
            for cartao in listar_cartoes()
            if cartao.status == "ATIVO"
        ]

        nomes_cartoes = [
            f"{cartao.nome} - {cartao.instituicao} (ID {cartao.id})"
            for cartao in cartoes
        ]

        # Buscar categorias de despesa ativas
        categorias = [
            categoria
            for categoria in listar_categorias_ativas()
            if categoria.tipo == "DESPESA"
        ]

        nomes_categorias = [
            f"{categoria.nome} (ID {categoria.id})"
            for categoria in categorias
        ]


        # Selecao de cartao
        label_cartao = ctk.CTkLabel(
            janela,
            text="Cartão de Crédito"
        )

        label_cartao.pack(
            padx=30,
            pady=(5, 0),
            anchor="w"
        )

        campo_cartao = ctk.CTkComboBox(
            janela,
            values=nomes_cartoes,
            state="readonly"
        )

        campo_cartao.pack(
            padx=30,
            pady=(5, 10),
            fill="x"
        )

        if nomes_cartoes:
            campo_cartao.set(nomes_cartoes[0])
        else:
            campo_cartao.set("")


        # Selecao de categoria
        label_categoria = ctk.CTkLabel(
            janela,
            text="Categoria da Despesa"
        )

        label_categoria.pack(
            padx=30,
            pady=(5, 0),
            anchor="w"
        )

        campo_categoria = ctk.CTkComboBox(
            janela,
            values=nomes_categorias,
            state="readonly"
        )

        campo_categoria.pack(
            padx=30,
            pady=(5, 10),
            fill="x"
        )

        if nomes_categorias:
            campo_categoria.set(nomes_categorias[0])
        else:
            campo_categoria.set("")


        # Descrição da compra
        entrada_descricao = ctk.CTkEntry(
            janela,
            placeholder_text="Descrição da compra"
        )

        entrada_descricao.pack(
            padx=30,
            pady=10,
            fill="x"
        )

        # Valor da compra
        entrada_valor = ctk.CTkEntry(
            janela,
            placeholder_text="Valor em reais"
        )

        entrada_valor.pack(
            padx=30,
            pady=10,
            fill="x"
        )

        # Data da compra
        entrada_data = ctk.CTkEntry(
            janela,
            placeholder_text="Data: AAAA-MM-DD"
        )

        entrada_data.insert(
            0,
            date.today().isoformat()
        )

        entrada_data.pack(
            padx=30,
            pady=10,
            fill="x"
        )

        # Observação
        entrada_observacao = ctk.CTkEntry(
            janela,
            placeholder_text="Observação (opcional)"
        )

        entrada_observacao.pack(
            padx=30,
            pady=10,
            fill="x"
        )
        

        def salvar_compra():
            try:
                # 1. Identificar o cartão selecionado
                cartao_selecionado = next(
                    (
                        cartao for cartao in cartoes
                        if (
                            f"{cartao.nome} - {cartao.instituicao} "
                            f"(ID {cartao.id})"
                        ) == campo_cartao.get()
                    ),
                    None
                )

                if cartao_selecionado is None:
                    raise ValueError(
                        "Selecione um cartão válido."
                    )

                # 2. Identificar a categoria selecionada
                categoria_selecionada = next(
                    (
                        categoria for categoria in categorias
                        if (
                            f"{categoria.nome} "
                            f"(ID {categoria.id})"
                        ) == campo_categoria.get()
                    ),
                    None
                )

                if categoria_selecionada is None:
                    raise ValueError(
                        "Selecione uma categoria válida."
                    )

                # 3. Validar a descrição
                descricao = entrada_descricao.get().strip()

                if not descricao:
                    raise ValueError(
                        "Informe a descrição da compra."
                    )

                # 4. Converter o valor em centavos
                valor_texto = (
                    entrada_valor.get()
                    .strip()
                    .replace(",", ".")
                )

                try:
                    valor_reais = Decimal(valor_texto)
                except InvalidOperation:
                    raise ValueError(
                        "Informe um valor válido."
                    )

                if (
                    not valor_reais.is_finite()
                    or valor_reais <= 0
                    or valor_reais.as_tuple().exponent < -2
                ):
                    raise ValueError(
                        "Informe um valor positivo "
                        "com até duas casas decimais."
                    )

                valor_centavos = int(valor_reais * 100)

                # 5. Obter data e observação
                data_compra = entrada_data.get().strip()
                observacao = (
                    entrada_observacao.get().strip() or None
                )

                # 6. Cadastrar a compra no banco
                cadastrar_compra(
                    cartao_id=cartao_selecionado.id,
                    categoria_id=categoria_selecionada.id,
                    descricao=descricao,
                    data_compra=data_compra,
                    valor_total=valor_centavos,
                    observacao=observacao
                )

                janela.destroy()
                
                self.carregar_compras()

                messagebox.showinfo(
                    "Compra cadastrada",
                    "Compra registrada com sucesso!"
                )

            except ValueError as erro:
                messagebox.showerror(
                    "Erro no cadastro",
                    str(erro)
                )

            except Exception as erro:
                messagebox.showerror(
                    "Erro inesperado",
                    str(erro)
                )
                

        botao_salvar = ctk.CTkButton(
            janela,
            text="Salvar Compra",
            command=salvar_compra
        )

        botao_salvar.pack(
            padx=30,
            pady=(10, 5),
            fill="x"
        )



        # Botão cancelar
        botao_cancelar = ctk.CTkButton(
            janela,
            text="Cancelar",
            fg_color="gray40",
            command=janela.destroy
        )

        botao_cancelar.pack(
            padx=30,
            pady=15,
            fill="x"
        )

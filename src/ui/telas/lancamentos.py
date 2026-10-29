import customtkinter as ctk

from services.lancamento_service import (
    listar_lancamentos,
    cadastrar_lancamento,
    cancelar_lancamento,
    atualizar_lancamento
)

from services.movimentacao_service import cadastrar_movimentacao

from services.categoria_service import listar_categorias_ativas


class TelaLancamentos(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.titulo = ctk.CTkLabel(
            self,
            text="Lançamentos",
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

        self.botao_novo_lancamento = ctk.CTkButton(
            self,
            text="Novo Lançamento",
            command=self.abrir_formulario_lancamento
        )

        self.botao_novo_lancamento.pack(
            padx=30,
            pady=(0, 20),
            anchor="nw"
        )

        self.lista_lancamentos = ctk.CTkScrollableFrame(
            self
        )

        self.lista_lancamentos.pack(
            padx=30,
            pady=(0, 30),
            fill="both",
            expand=True
        )

        self.carregar_lancamentos()

    def atualizar_lista(self):
        for widget in self.lista_lancamentos.winfo_children():
            widget.destroy()

        self.carregar_lancamentos()

    def carregar_lancamentos(self):
        lancamentos = listar_lancamentos()

        for lancamento in lancamentos:
            linha = ctk.CTkFrame(
                self.lista_lancamentos
            )

            linha.pack(
                padx=10,
                pady=8,
                fill="x"
            )

            texto = (
                f"{lancamento.descricao} | "
                f"{lancamento.tipo} | "
                f"R$ {lancamento.valor_previsto / 100:.2f}".replace(
                    ".", ",") + " | "
                f"{lancamento.data_prevista} | "
                f"{lancamento.status}"
            )

            label = ctk.CTkLabel(
                linha,
                text=texto,
                anchor="w"
            )

            label.pack(
                side="left",
                padx=10,
                pady=10,
                fill="x",
                expand=True
            )

            if lancamento.status == "PENDENTE":
                botao_editar = ctk.CTkButton(
                    linha,
                    text="Editar",
                    width=80,
                    command=lambda l=lancamento: self.abrir_edicao_lancamento(
                        l)
                )
                
                texto_botao = (
                    "Receber"
                    if lancamento.tipo == "RECEITA"
                    else "Pagar"
                )

                botao_efetivar = ctk.CTkButton(
                    linha,
                    text=texto_botao,
                    width=80,
                    command=lambda l=lancamento: self.abrir_movimentacao(l)
                )

                botao_efetivar.pack(
                    side="right",
                    padx=5,
                    pady=10
                )

                botao_editar.pack(
                    side="right",
                    padx=5,
                    pady=10
                )

                botao_cancelar = ctk.CTkButton(
                    linha,
                    text="Cancelar",
                    width=90,
                    command=lambda l=lancamento: self.cancelar_lancamento_interface(
                        l)
                )

                botao_cancelar.pack(
                    side="right",
                    padx=5,
                    pady=10
                )

    def cancelar_lancamento_interface(self, lancamento):
        try:
            cancelar_lancamento(
                lancamento.id
            )

            self.atualizar_lista()

        except ValueError as erro:
            print(erro)

    def abrir_formulario_lancamento(self):
        janela = ctk.CTkToplevel(self)

        janela.title("Novo Lançamento")
        janela.geometry("450x560")

        janela.transient(self)
        janela.grab_set()
        janela.focus_force()

        titulo = ctk.CTkLabel(
            janela,
            text="Cadastrar Lançamento",
            font=ctk.CTkFont(
                size=22,
                weight="bold"
            )
        )

        titulo.pack(
            pady=(30, 20)
        )

        entrada_descricao = ctk.CTkEntry(
            janela,
            placeholder_text="Descrição"
        )

        entrada_descricao.pack(
            padx=30,
            pady=10,
            fill="x"
        )

        campo_tipo = ctk.CTkComboBox(
            janela,
            values=[
                "RECEITA",
                "DESPESA"
            ],
            state="readonly"
        )

        campo_tipo.pack(
            padx=30,
            pady=10,
            fill="x"
        )

        entrada_valor = ctk.CTkEntry(
            janela,
            placeholder_text="Valor em reais"
        )

        entrada_valor.pack(
            padx=30,
            pady=10,
            fill="x"
        )

        entrada_data = ctk.CTkEntry(
            janela,
            placeholder_text="Data prevista: AAAA-MM-DD"
        )

        entrada_data.pack(
            padx=30,
            pady=10,
            fill="x"
        )

        categorias = listar_categorias_ativas()

        def atualizar_categorias(tipo_selecionado):
            nomes_categorias = []

            for categoria in categorias:
                if categoria.tipo == tipo_selecionado:
                    nomes_categorias.append(
                        f"{categoria.nome} - {categoria.tipo}"
                    )

            campo_categoria.configure(
                values=nomes_categorias
            )

            if nomes_categorias:
                campo_categoria.set(
                    nomes_categorias[0]
                )
            else:
                campo_categoria.set("")

        nomes_categorias = []

        tipo_inicial = campo_tipo.get()

        for categoria in categorias:
            if categoria.tipo == tipo_inicial:
                nomes_categorias.append(
                    f"{categoria.nome} - {categoria.tipo}"
                )

        campo_categoria = ctk.CTkComboBox(
            janela,
            values=nomes_categorias,
            state="readonly"
        )

        campo_categoria.pack(
            padx=30,
            pady=10,
            fill="x"
        )

        if nomes_categorias:
            campo_categoria.set(
                nomes_categorias[0]
            )

        campo_tipo.configure(
            command=atualizar_categorias
        )

        entrada_observacao = ctk.CTkEntry(
            janela,
            placeholder_text="Observação"
        )

        entrada_observacao.pack(
            padx=30,
            pady=10,
            fill="x"
        )

        mensagem_erro = ctk.CTkLabel(
            janela,
            text=""
        )

        mensagem_erro.pack(
            padx=30,
            pady=(5, 0)
        )

        def salvar():
            descricao = entrada_descricao.get()
            tipo = campo_tipo.get()
            valor_texto = entrada_valor.get()
            data_prevista = entrada_data.get()
            categoria_selecionada = campo_categoria.get()
            observacao = entrada_observacao.get()

            try:
                valor_reais = float(
                    valor_texto.replace(",", ".")
                )

                valor_centavos = int(
                    round(valor_reais * 100)
                )

                categoria_encontrada = None

                for categoria in categorias:
                    texto_categoria = (
                        f"{categoria.nome} - {categoria.tipo}"
                    )

                    if texto_categoria == categoria_selecionada:
                        categoria_encontrada = categoria
                        break

                if categoria_encontrada is None:
                    mensagem_erro.configure(
                        text="Selecione uma categoria válida."
                    )
                    return

                cadastrar_lancamento(
                    tipo=tipo,
                    descricao=descricao,
                    valor_previsto=valor_centavos,
                    data_prevista=data_prevista,
                    categoria_id=categoria_encontrada.id,
                    observacao=observacao
                )

                janela.destroy()

                self.atualizar_lista()

            except ValueError as erro:
                mensagem_erro.configure(
                    text=str(erro)
                )

        botao_salvar = ctk.CTkButton(
            janela,
            text="Salvar",
            command=salvar
        )

        botao_salvar.pack(
            padx=30,
            pady=20,
            fill="x"
        )

    def abrir_edicao_lancamento(self, lancamento):
        janela = ctk.CTkToplevel(self)

        janela.title("Editar Lançamento")
        janela.geometry("450x600")

        janela.transient(self)
        janela.grab_set()
        janela.focus_force()

        titulo = ctk.CTkLabel(
            janela,
            text="Editar Lançamento",
            font=ctk.CTkFont(
                size=22,
                weight="bold"
            )
        )

        titulo.pack(
            pady=(30, 20)
        )

        entrada_descricao = ctk.CTkEntry(
            janela
        )

        entrada_descricao.insert(
            0,
            lancamento.descricao
        )

        entrada_descricao.pack(
            padx=30,
            pady=10,
            fill="x"
        )

        campo_tipo = ctk.CTkComboBox(
            janela,
            values=[
                "RECEITA",
                "DESPESA"
            ],
            state="readonly"
        )

        campo_tipo.set(
            lancamento.tipo
        )

        campo_tipo.pack(
            padx=30,
            pady=10,
            fill="x"
        )

        entrada_valor = ctk.CTkEntry(
            janela
        )

        entrada_valor.insert(
            0,
            str(
                lancamento.valor_previsto / 100
            ).replace(".", ",")
        )

        entrada_valor.pack(
            padx=30,
            pady=10,
            fill="x"
        )

        entrada_data = ctk.CTkEntry(
            janela
        )

        entrada_data.insert(
            0,
            lancamento.data_prevista
        )

        entrada_data.pack(
            padx=30,
            pady=10,
            fill="x"
        )

        categorias = listar_categorias_ativas()

        def atualizar_categorias_edicao(tipo_selecionado):
            nomes_categorias = []

            for categoria in categorias:
                if categoria.tipo == tipo_selecionado:
                    nomes_categorias.append(
                        f"{categoria.nome} - {categoria.tipo}"
                    )

            campo_categoria.configure(
                values=nomes_categorias
            )

            if nomes_categorias:
                campo_categoria.set(
                    nomes_categorias[0]
                )
            else:
                campo_categoria.set("")

        nomes_categorias = []

        for categoria in categorias:
            if categoria.tipo == lancamento.tipo:
                nomes_categorias.append(
                    f"{categoria.nome} - {categoria.tipo}"
                )

        campo_categoria = ctk.CTkComboBox(
            janela,
            values=nomes_categorias,
            state="readonly"
        )

        campo_categoria.pack(
            padx=30,
            pady=10,
            fill="x"
        )

        for categoria in categorias:
            if categoria.id == lancamento.categoria_id:
                campo_categoria.set(
                    f"{categoria.nome} - {categoria.tipo}"
                )
                break

        campo_tipo.configure(
            command=atualizar_categorias_edicao
        )

        entrada_observacao = ctk.CTkEntry(
            janela
        )

        if lancamento.observacao:
            entrada_observacao.insert(
                0,
                lancamento.observacao
            )

        entrada_observacao.pack(
            padx=30,
            pady=10,
            fill="x"
        )

        mensagem_erro = ctk.CTkLabel(
            janela,
            text=""
        )

        mensagem_erro.pack(
            padx=30,
            pady=(5, 0)
        )

        def salvar_edicao():
            descricao = entrada_descricao.get()
            tipo = campo_tipo.get()
            valor_texto = entrada_valor.get()
            data_prevista = entrada_data.get()
            categoria_selecionada = campo_categoria.get()
            observacao = entrada_observacao.get()

            try:
                valor_reais = float(
                    valor_texto.replace(",", ".")
                )

                valor_centavos = int(
                    round(valor_reais * 100)
                )

                categoria_encontrada = None

                for categoria in categorias:
                    texto_categoria = (
                        f"{categoria.nome} - {categoria.tipo}"
                    )

                    if texto_categoria == categoria_selecionada:
                        categoria_encontrada = categoria
                        break

                if categoria_encontrada is None:
                    mensagem_erro.configure(
                        text="Selecione uma categoria válida."
                    )
                    return

                atualizar_lancamento(
                    lancamento_id=lancamento.id,
                    tipo=tipo,
                    descricao=descricao,
                    valor_previsto=valor_centavos,
                    data_prevista=data_prevista,
                    categoria_id=categoria_encontrada.id,
                    status=lancamento.status,
                    observacao=observacao
                )

                janela.destroy()

                self.atualizar_lista()

            except ValueError as erro:
                mensagem_erro.configure(
                    text=str(erro)
                )

        botao_salvar = ctk.CTkButton(
            janela,
            text="Salvar Alterações",
            command=salvar_edicao
        )

        botao_salvar.pack(
            padx=30,
            pady=20,
            fill="x"
        )
        
    def abrir_movimentacao(self, lancamento):
        janela = ctk.CTkToplevel(self)

        janela.title("Registrar Movimentação")
        janela.geometry("450x500")

        janela.transient(self)
        janela.grab_set()
        janela.focus_force()
        titulo = ctk.CTkLabel(
            janela,
            text=(
                "Registrar Recebimento"
                if lancamento.tipo == "RECEITA"
                else "Registrar Pagamento"
            ),
            font=ctk.CTkFont(
                size=22,
                weight="bold"
            )
        )

        titulo.pack(
            pady=(30, 20)
        )
        entrada_valor = ctk.CTkEntry(
            janela,
            placeholder_text="Valor pago ou recebido"
        )

        entrada_valor.insert(
            0,
            f"{lancamento.valor_previsto / 100:.2f}".replace(".", ",")
        )

        entrada_valor.pack(
            padx=30,
            pady=10,
            fill="x"
        )
        entrada_data = ctk.CTkEntry(
            janela,
            placeholder_text="Data: AAAA-MM-DD"
        )

        entrada_data.pack(
            padx=30,
            pady=10,
            fill="x"
        )
        campo_forma = ctk.CTkComboBox(
            janela,
            values=[
                "PIX",
                "DINHEIRO",
                "DEBITO",
                "TRANSFERENCIA",
                "BOLETO",
                "OUTRO"
            ],
            state="readonly"
        )

        campo_forma.set("PIX")

        campo_forma.pack(
            padx=30,
            pady=10,
            fill="x"
        )
        entrada_observacao = ctk.CTkEntry(
            janela,
            placeholder_text="Observação (opcional)"
        )

        entrada_observacao.pack(
            padx=30,
            pady=10,
            fill="x"
        )

        mensagem_erro = ctk.CTkLabel(
            janela,
            text="",
            text_color="#FF6B6B",
            wraplength=380
        )

        mensagem_erro.pack(
            padx=30,
            pady=(5, 0)
        )
        def confirmar_movimentacao():
            valor_texto = entrada_valor.get()
            data = entrada_data.get()
            forma = campo_forma.get()
            observacao = entrada_observacao.get()

            try:
                valor_reais = float(
                    valor_texto.replace(",", ".")
                )

                valor_centavos = int(
                    round(valor_reais * 100)
                )

                cadastrar_movimentacao(
                    lancamento_id=lancamento.id,
                    valor=valor_centavos,
                    data_movimentacao=data,
                    forma=forma,
                    observacao=observacao
                )

                janela.destroy()
                self.atualizar_lista()

            except ValueError as erro:
                mensagem_erro.configure(
                    text=str(erro)
                )
        botao_confirmar = ctk.CTkButton(
            janela,
            text=(
                "Confirmar Recebimento"
                if lancamento.tipo == "RECEITA"
                else "Confirmar Pagamento"
            ),
            command=confirmar_movimentacao
        )

        botao_confirmar.pack(
            padx=30,
            pady=20,
            fill="x"
        )
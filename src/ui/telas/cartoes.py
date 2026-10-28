import customtkinter as ctk

from services.cartao_service import (
    listar_cartoes,
    cadastrar_cartao,
    atualizar_cartao,
    inativar_cartao,
    reativar_cartao
)


class TelaCartoes(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.botao_novo_cartao = ctk.CTkButton(
            self,
            text="Novo Cartão",
            command=self.abrir_formulario_cartao
        )

        self.botao_novo_cartao.pack(
            padx=30,
            pady=(0, 20),
            anchor="nw"
        )

        self.titulo = ctk.CTkLabel(
            self,
            text="Cartões",
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

        self.lista_cartoes = ctk.CTkScrollableFrame(
            self
        )

        self.lista_cartoes.pack(
            padx=30,
            pady=(0, 30),
            fill="both",
            expand=True
        )

        self.carregar_cartoes()

    def carregar_cartoes(self):
        cartoes = listar_cartoes()

        for cartao in cartoes:
            linha = ctk.CTkFrame(
                self.lista_cartoes
            )

            linha.pack(
                padx=10,
                pady=8,
                fill="x"
            )

            limite_formatado = (
                f"R$ {cartao.limite_total / 100:.2f}"
                .replace(".", ",")
            )

            texto = (
                f"{cartao.nome} | "
                f"{cartao.instituicao} | "
                f"{limite_formatado} | "
                f"Fechamento: {cartao.dia_fechamento} | "
                f"Vencimento: {cartao.dia_vencimento} | "
                f"{cartao.status}"
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
            
            if cartao.status == "ATIVO":
                botao_inativar = ctk.CTkButton(
                    linha,
                    text="Inativar",
                    width=90,
                    command=lambda c=cartao: self.inativar_cartao_interface(c)
                )

                botao_inativar.pack(
                    side="right",
                    padx=5,
                    pady=10
                )
                
                botao_editar = ctk.CTkButton(
                    linha,
                    text="Editar",
                    width=80,
                    command=lambda c=cartao: self.abrir_edicao_cartao(c)
                )

                botao_editar.pack(
                    side="right",
                    padx=5,
                    pady=10
                )
                
            else:
                botao_reativar = ctk.CTkButton(
                    linha,
                    text="Reativar",
                    width=90,
                    command=lambda c=cartao: self.reativar_cartao_interface(c)
                )

                botao_reativar.pack(
                    side="right",
                    padx=5,
                    pady=10
                )
                
    def inativar_cartao_interface(self, cartao):
        try:
            inativar_cartao(
                cartao.id
            )

            self.atualizar_lista()

        except ValueError as erro:
            print(erro)
            
    def reativar_cartao_interface(self, cartao):
        try:
            reativar_cartao(
                cartao.id
            )

            self.atualizar_lista()

        except ValueError as erro:
            print(erro)
            
    def abrir_edicao_cartao(self, cartao):
        janela = ctk.CTkToplevel(self)

        janela.title("Editar Cartão")
        janela.geometry("450x620")

        janela.transient(self)
        janela.grab_set()
        janela.focus_force()

        titulo = ctk.CTkLabel(
            janela,
            text="Editar Cartão",
            font=ctk.CTkFont(
                size=22,
                weight="bold"
            )
        )

        titulo.pack(
            pady=(30, 20)
        )

        entrada_nome = ctk.CTkEntry(
            janela
        )

        entrada_nome.insert(
            0,
            cartao.nome
        )

        entrada_nome.pack(
            padx=30,
            pady=10,
            fill="x"
        )

        entrada_instituicao = ctk.CTkEntry(
            janela
        )

        entrada_instituicao.insert(
            0,
            cartao.instituicao
        )

        entrada_instituicao.pack(
            padx=30,
            pady=10,
            fill="x"
        )

        entrada_limite = ctk.CTkEntry(
            janela
        )

        entrada_limite.insert(
            0,
            str(cartao.limite_total / 100).replace(".", ",")
        )

        entrada_limite.pack(
            padx=30,
            pady=10,
            fill="x"
        )

        entrada_fechamento = ctk.CTkEntry(
            janela
        )

        entrada_fechamento.insert(
            0,
            str(cartao.dia_fechamento)
        )

        entrada_fechamento.pack(
            padx=30,
            pady=10,
            fill="x"
        )

        entrada_vencimento = ctk.CTkEntry(
            janela
        )

        entrada_vencimento.insert(
            0,
            str(cartao.dia_vencimento)
        )

        entrada_vencimento.pack(
            padx=30,
            pady=10,
            fill="x"
        )

        campo_status = ctk.CTkComboBox(
            janela,
            values=[
                "ATIVO",
                "INATIVO"
            ],
            state="readonly"
        )

        campo_status.set(
            cartao.status
        )

        campo_status.pack(
            padx=30,
            pady=10,
            fill="x"
        )

        entrada_observacao = ctk.CTkEntry(
            janela
        )

        if cartao.observacao:
            entrada_observacao.insert(
                0,
                cartao.observacao
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
            nome = entrada_nome.get()
            instituicao = entrada_instituicao.get()
            limite_texto = entrada_limite.get()
            dia_fechamento_texto = entrada_fechamento.get()
            dia_vencimento_texto = entrada_vencimento.get()
            status = campo_status.get()
            observacao = entrada_observacao.get()

            try:
                limite_reais = float(
                    limite_texto.replace(",", ".")
                )

                limite_centavos = int(
                    round(limite_reais * 100)
                )

                dia_fechamento = int(
                    dia_fechamento_texto
                )

                dia_vencimento = int(
                    dia_vencimento_texto
                )

                atualizar_cartao(
                    cartao_id=cartao.id,
                    nome=nome,
                    instituicao=instituicao,
                    limite_total=limite_centavos,
                    dia_fechamento=dia_fechamento,
                    dia_vencimento=dia_vencimento,
                    status=status,
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

    def abrir_formulario_cartao(self):
        janela = ctk.CTkToplevel(self)

        janela.title("Novo Cartão")
        janela.geometry("450x580")

        janela.transient(self)
        janela.grab_set()
        janela.focus_force()

        titulo = ctk.CTkLabel(
            janela,
            text="Cadastrar Cartão",
            font=ctk.CTkFont(
                size=22,
                weight="bold"
            )
        )

        titulo.pack(
            pady=(30, 20)
        )

        entrada_nome = ctk.CTkEntry(
            janela,
            placeholder_text="Nome do cartão"
        )

        entrada_nome.pack(
            padx=30,
            pady=10,
            fill="x"
        )

        entrada_instituicao = ctk.CTkEntry(
            janela,
            placeholder_text="Instituição"
        )

        entrada_instituicao.pack(
            padx=30,
            pady=10,
            fill="x"
        )

        entrada_limite = ctk.CTkEntry(
            janela,
            placeholder_text="Limite total em reais"
        )

        entrada_limite.pack(
            padx=30,
            pady=10,
            fill="x"
        )

        entrada_fechamento = ctk.CTkEntry(
            janela,
            placeholder_text="Dia de fechamento"
        )

        entrada_fechamento.pack(
            padx=30,
            pady=10,
            fill="x"
        )

        entrada_vencimento = ctk.CTkEntry(
            janela,
            placeholder_text="Dia de vencimento"
        )

        entrada_vencimento.pack(
            padx=30,
            pady=10,
            fill="x"
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
            nome = entrada_nome.get()
            instituicao = entrada_instituicao.get()
            limite_texto = entrada_limite.get()
            dia_fechamento_texto = entrada_fechamento.get()
            dia_vencimento_texto = entrada_vencimento.get()
            observacao = entrada_observacao.get()

            try:
                limite_reais = float(
                    limite_texto.replace(",", ".")
                )

                limite_centavos = int(
                    round(limite_reais * 100)
                )

                dia_fechamento = int(
                    dia_fechamento_texto
                )

                dia_vencimento = int(
                    dia_vencimento_texto
                )

                cadastrar_cartao(
                    nome=nome,
                    instituicao=instituicao,
                    limite_total=limite_centavos,
                    dia_fechamento=dia_fechamento,
                    dia_vencimento=dia_vencimento,
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

    def atualizar_lista(self):
        for widget in self.lista_cartoes.winfo_children():
            widget.destroy()

        self.carregar_cartoes()

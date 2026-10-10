import customtkinter as ctk

from services.categoria_service import (
    listar_categorias,
    cadastrar_categoria,
    atualizar_categoria,
    inativar_categoria
)


class TelaCategorias(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.titulo = ctk.CTkLabel(
            self,
            text="Categorias",
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

        self.botao_nova_categoria = ctk.CTkButton(
            self,
            text="Nova Categoria",
            command=self.abrir_formulario_categoria
        )

        self.botao_nova_categoria.pack(
            padx=30,
            pady=(0, 20),
            anchor="nw"
        )

        self.lista_categorias = ctk.CTkScrollableFrame(
            self
        )

        self.lista_categorias.pack(
            padx=30,
            pady=(0, 30),
            fill="both",
            expand=True
        )

        self.carregar_categorias()

    def carregar_categorias(self):
        categorias = listar_categorias()

        for categoria in categorias:
            linha = ctk.CTkFrame(
                self.lista_categorias
            )

            linha.pack(
                padx=10,
                pady=8,
                fill="x"
            )

            texto = (
                f"{categoria.nome} | "
                f"{categoria.tipo} | "
                f"{categoria.status}"
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

            botao_editar = ctk.CTkButton(
                linha,
                text="Editar",
                width=80,
                command=lambda c=categoria: self.abrir_edicao_categoria(c)
            )

            botao_editar.pack(
                side="right",
                padx=5,
                pady=10
            )

            botao_inativar = ctk.CTkButton(
                linha,
                text="Inativar",
                width=80,
                command=lambda c=categoria: self.inativar_categoria_interface(c)
            )

            botao_inativar.pack(
                side="right",
                padx=5,
                pady=10
            )

    def abrir_formulario_categoria(self):
        janela = ctk.CTkToplevel(self)

        janela.title("Nova Categoria")
        janela.geometry("400x420")

        titulo = ctk.CTkLabel(
            janela,
            text="Cadastrar Categoria",
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
            placeholder_text="Nome da categoria"
        )

        entrada_nome.pack(
            padx=30,
            pady=10,
            fill="x"
        )

        campo_tipo = ctk.CTkComboBox(
            janela,
            values=[
                "RECEITA",
                "DESPESA"
            ]
        )

        campo_tipo.pack(
            padx=30,
            pady=10,
            fill="x"
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
            tipo = campo_tipo.get()
            descricao = entrada_descricao.get()

            try:
                cadastrar_categoria(
                    nome=nome,
                    tipo=tipo,
                    descricao=descricao
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
        for widget in self.lista_categorias.winfo_children():
            widget.destroy()

        self.carregar_categorias()
        
    def inativar_categoria_interface(self, categoria):
        try:
            inativar_categoria(categoria.id)

            self.atualizar_lista()

        except ValueError as erro:
            print(erro)
            
    def abrir_edicao_categoria(self, categoria):
        janela = ctk.CTkToplevel(self)

        janela.title("Editar Categoria")
        janela.geometry("400x460")

        titulo = ctk.CTkLabel(
            janela,
            text="Editar Categoria",
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
            categoria.nome
        )

        entrada_nome.pack(
            padx=30,
            pady=10,
            fill="x"
        )

        campo_tipo = ctk.CTkComboBox(
            janela,
            values=[
                "RECEITA",
                "DESPESA"
            ]
        )

        campo_tipo.set(
            categoria.tipo
        )

        campo_tipo.pack(
            padx=30,
            pady=10,
            fill="x"
        )

        entrada_descricao = ctk.CTkEntry(
            janela
        )

        if categoria.descricao:
            entrada_descricao.insert(
                0,
                categoria.descricao
            )

        entrada_descricao.pack(
            padx=30,
            pady=10,
            fill="x"
        )

        campo_status = ctk.CTkComboBox(
            janela,
            values=[
                "ATIVA",
                "INATIVA"
            ]
        )

        campo_status.set(
            categoria.status
        )

        campo_status.pack(
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
            try:
                atualizar_categoria(
                    categoria_id=categoria.id,
                    nome=entrada_nome.get(),
                    tipo=campo_tipo.get(),
                    descricao=entrada_descricao.get(),
                    status=campo_status.get()
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
import customtkinter as ctk

from services.cartao_service import (
    listar_cartoes,
    cadastrar_cartao
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
                padx=10,
                pady=10,
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
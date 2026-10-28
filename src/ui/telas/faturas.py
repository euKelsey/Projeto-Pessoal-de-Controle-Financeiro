import customtkinter as ctk

from services.fatura_service import (
    listar_faturas,
    cadastrar_fatura
)

from services.cartao_service import listar_cartoes


class TelaFaturas(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.titulo = ctk.CTkLabel(
            self,
            text="Faturas",
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

        self.botao_nova_fatura = ctk.CTkButton(
            self,
            text="Nova Fatura",
            command=self.abrir_formulario_fatura
        )

        self.botao_nova_fatura.pack(
            padx=30,
            pady=(0, 20),
            anchor="nw"
        )

        self.lista_faturas = ctk.CTkScrollableFrame(
            self
        )

        self.lista_faturas.pack(
            padx=30,
            pady=(0, 30),
            fill="both",
            expand=True
        )

        self.carregar_faturas()

    def carregar_faturas(self):
        faturas = listar_faturas()
        
        cartoes = listar_cartoes()

        nomes_cartoes = {}

        for cartao in cartoes:
            nomes_cartoes[cartao.id] = cartao.nome

        for fatura in faturas:
            linha = ctk.CTkFrame(
                self.lista_faturas
            )

            linha.pack(
                padx=10,
                pady=8,
                fill="x"
            )
            
            nome_cartao = nomes_cartoes.get(
                fatura.cartao_id,
                "Cartão não encontrado"
            )

            texto = (
                f"{nome_cartao} | "
                f"Mês: {fatura.mes_referencia} | "
                f"Fechamento: {fatura.data_fechamento} | "
                f"Vencimento: {fatura.data_vencimento} | "
                f"{fatura.status}"
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

    def abrir_formulario_fatura(self):
        janela = ctk.CTkToplevel(self)

        janela.title("Nova Fatura")
        janela.geometry("450x500")

        janela.transient(self)
        janela.grab_set()
        janela.focus_force()

        titulo = ctk.CTkLabel(
            janela,
            text="Cadastrar Fatura",
            font=ctk.CTkFont(
                size=22,
                weight="bold"
            )
        )

        titulo.pack(
            pady=(30, 20)
        )

        cartoes = listar_cartoes()

        cartoes_ativos = []

        for cartao in cartoes:
            if cartao.status == "ATIVO":
                cartoes_ativos.append(cartao)

        nomes_cartoes = []

        for cartao in cartoes_ativos:
            nomes_cartoes.append(
                f"{cartao.nome} - {cartao.instituicao}"
            )

        campo_cartao = ctk.CTkComboBox(
            janela,
            values=nomes_cartoes,
            state="readonly"
        )

        campo_cartao.pack(
            padx=30,
            pady=10,
            fill="x"
        )

        if nomes_cartoes:
            campo_cartao.set(
                nomes_cartoes[0]
            )

        entrada_mes = ctk.CTkEntry(
            janela,
            placeholder_text="Mês de referência: AAAA-MM"
        )

        entrada_mes.pack(
            padx=30,
            pady=10,
            fill="x"
        )

        entrada_fechamento = ctk.CTkEntry(
            janela,
            placeholder_text="Data de fechamento: AAAA-MM-DD"
        )

        entrada_fechamento.pack(
            padx=30,
            pady=10,
            fill="x"
        )

        entrada_vencimento = ctk.CTkEntry(
            janela,
            placeholder_text="Data de vencimento: AAAA-MM-DD"
        )

        entrada_vencimento.pack(
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
            cartao_selecionado = campo_cartao.get()
            mes_referencia = entrada_mes.get()
            data_fechamento = entrada_fechamento.get()
            data_vencimento = entrada_vencimento.get()

            try:
                cartao_encontrado = None

                for cartao in cartoes_ativos:
                    texto_cartao = (
                        f"{cartao.nome} - {cartao.instituicao}"
                    )

                    if texto_cartao == cartao_selecionado:
                        cartao_encontrado = cartao
                        break

                if cartao_encontrado is None:
                    mensagem_erro.configure(
                        text="Selecione um cartão válido."
                    )
                    return

                cadastrar_fatura(
                    cartao_id=cartao_encontrado.id,
                    mes_referencia=mes_referencia,
                    data_fechamento=data_fechamento,
                    data_vencimento=data_vencimento
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
        for widget in self.lista_faturas.winfo_children():
            widget.destroy()

        self.carregar_faturas()

import customtkinter as ctk
from datetime import date
from tkinter import messagebox

from services.fatura_service import (
    listar_faturas,
    cadastrar_fatura,
    obter_total_fatura,
    atualizar_faturas_automaticamente,
    atualizar_fatura,
    pagar_fatura
)

from repositories.lancamento_repository import buscar_por_fatura_id

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
        atualizar_faturas_automaticamente()
        
        faturas = listar_faturas()

        cartoes = listar_cartoes()

        nomes_cartoes = {}

        for cartao in cartoes:
            nomes_cartoes[cartao.id] = cartao.nome

        for fatura in faturas:

            total_centavos = obter_total_fatura(fatura.id)

            total_formatado = (
                f"R$ {total_centavos / 100:,.2f}"
                .replace(",", "X")
                .replace(".", ",")
                .replace("X", ".")
            )

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
                f"{total_formatado} | "
                f"{fatura.status}"
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


            if fatura.status == "ABERTA":
                botao_editar = ctk.CTkButton(
                    linha,
                    text="Editar",
                    width=80,
                    command=lambda f=fatura: self.abrir_edicao_fatura(f)
                )

                botao_editar.pack(
                    side="right",
                    padx=5,
                    pady=10
                )
                

            if fatura.status == "FECHADA":
                lancamento = buscar_por_fatura_id(fatura.id)

                if (
                    lancamento is not None
                    and lancamento.status == "PENDENTE"
                ):
                    botao_pagar = ctk.CTkButton(
                        linha,
                        text="Pagar",
                        width=80,
                        command=lambda f=fatura: self.abrir_pagamento_fatura(f)
                    )

                    botao_pagar.pack(
                        side="right",
                        padx=5,
                        pady=10
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

    def abrir_edicao_fatura(self, fatura):
        janela = ctk.CTkToplevel(self)

        janela.title("Editar Fatura")
        janela.geometry("450x500")

        janela.transient(self)
        janela.grab_set()
        janela.focus_force()
        titulo = ctk.CTkLabel(
            janela,
            text="Editar Fatura",
            font=ctk.CTkFont(
                size=22,
                weight="bold"
            )
        )

        titulo.pack(
            pady=(30, 20)
        )
        entrada_mes = ctk.CTkEntry(
            janela
        )

        entrada_mes.insert(
            0,
            fatura.mes_referencia
        )

        entrada_mes.pack(
            padx=30,
            pady=10,
            fill="x"
        )
        entrada_fechamento = ctk.CTkEntry(
            janela
        )

        entrada_fechamento.insert(
            0,
            fatura.data_fechamento
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
            fatura.data_vencimento
        )

        entrada_vencimento.pack(
            padx=30,
            pady=10,
            fill="x"
        )
        campo_status = ctk.CTkComboBox(
            janela,
            values=[
                "ABERTA",
                "FECHADA"
            ],
            state="readonly"
        )

        campo_status.set(
            fatura.status
        )

        campo_status.pack(
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

        def salvar_edicao():
            mes_referencia = entrada_mes.get()
            data_fechamento = entrada_fechamento.get()
            data_vencimento = entrada_vencimento.get()
            status = campo_status.get()

            try:
                atualizar_fatura(
                    fatura_id=fatura.id,
                    mes_referencia=mes_referencia,
                    data_fechamento=data_fechamento,
                    data_vencimento=data_vencimento,
                    status=status
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
        

    def abrir_pagamento_fatura(self, fatura):
        janela = ctk.CTkToplevel(self)
        janela.title("Pagar Fatura")
        janela.geometry("450x480")

        janela.transient(self)
        janela.grab_set()
        janela.focus_force()

        titulo = ctk.CTkLabel(
            janela,
            text="Pagamento de Fatura",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        titulo.pack(pady=(25, 15))

        total_centavos = obter_total_fatura(fatura.id)

        total_formatado = (
            f"R$ {total_centavos / 100:,.2f}"
            .replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )

        informacoes = ctk.CTkLabel(
            janela,
            text=(
                f"Fatura: {fatura.mes_referencia}\n"
                f"Valor: {total_formatado}"
            ),
            font=ctk.CTkFont(size=16)
        )
        informacoes.pack(pady=10)

        entrada_data = ctk.CTkEntry(
            janela,
            placeholder_text="Data: AAAA-MM-DD"
        )
        entrada_data.insert(0, date.today().isoformat())
        entrada_data.pack(padx=30, pady=10, fill="x")

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
        campo_forma.pack(padx=30, pady=10, fill="x")

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
        mensagem_erro.pack(padx=30, pady=5)

        def confirmar_pagamento():
            try:
                pagar_fatura(
                    fatura_id=fatura.id,
                    data_pagamento=entrada_data.get(),
                    forma=campo_forma.get(),
                    observacao=entrada_observacao.get() or None
                )

                janela.destroy()
                self.atualizar_lista()

                messagebox.showinfo(
                    "Pagamento registrado",
                    "A fatura foi paga com sucesso."
                )

            except ValueError as erro:
                mensagem_erro.configure(text=str(erro))

            except Exception as erro:
                mensagem_erro.configure(
                    text=f"Erro ao registrar pagamento: {erro}"
                )

        botao_confirmar = ctk.CTkButton(
            janela,
            text="Confirmar Pagamento",
            command=confirmar_pagamento
        )
        botao_confirmar.pack(
            padx=30,
            pady=(10, 5),
            fill="x"
        )

        botao_cancelar = ctk.CTkButton(
            janela,
            text="Cancelar",
            fg_color="gray40",
            command=janela.destroy
        )
        botao_cancelar.pack(
            padx=30,
            pady=5,
            fill="x"
        )


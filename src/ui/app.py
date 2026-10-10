import customtkinter as ctk

from ui.telas.categorias import TelaCategorias


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Controle Financeiro")
        self.geometry("1200x700")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.menu_lateral = ctk.CTkFrame(
            self,
            width=220,
            corner_radius=0
        )

        self.menu_lateral.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        self.area_principal = ctk.CTkFrame(
            self,
            corner_radius=0
        )

        self.area_principal.grid(
            row=0,
            column=1,
            sticky="nsew"
        )

        self.titulo_menu = ctk.CTkLabel(
            self.menu_lateral,
            text="Controle Financeiro",
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            )
        )

        self.titulo_menu.pack(
            pady=(30, 30),
            padx=20
        )

        self.botao_dashboard = ctk.CTkButton(
            self.menu_lateral,
            text="Dashboard"
        )

        self.botao_dashboard.pack(
            padx=20,
            pady=10,
            fill="x"
        )

        self.botao_lancamentos = ctk.CTkButton(
            self.menu_lateral,
            text="Lançamentos"
        )

        self.botao_lancamentos.pack(
            padx=20,
            pady=10,
            fill="x"
        )

        self.botao_cartoes = ctk.CTkButton(
            self.menu_lateral,
            text="Cartões"
        )

        self.botao_cartoes.pack(
            padx=20,
            pady=10,
            fill="x"
        )

        self.botao_categorias = ctk.CTkButton(
            self.menu_lateral,
            text="Categorias",
            command=self.mostrar_categorias
        )

        self.botao_categorias.pack(
            padx=20,
            pady=10,
            fill="x"
        )

        self.botao_faturas = ctk.CTkButton(
            self.menu_lateral,
            text="Faturas"
        )

        self.botao_faturas.pack(
            padx=20,
            pady=10,
            fill="x"
        )

        self.titulo_principal = ctk.CTkLabel(
            self.area_principal,
            text="Dashboard",
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        )

        self.titulo_principal.pack(
            padx=30,
            pady=30,
            anchor="nw"
        )

    def limpar_area_principal(self):
        for widget in self.area_principal.winfo_children():
            widget.destroy()

    def mostrar_categorias(self):
        self.limpar_area_principal()

        tela = TelaCategorias(self.area_principal)

        tela.pack(
            fill="both",
            expand=True
        )
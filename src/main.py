from database.conexao import inicializar_banco
from services.fatura_service import atualizar_faturas_automaticamente
from ui.app import App



inicializar_banco()

quantidade_fechada = atualizar_faturas_automaticamente()

print(
    f"Faturas fechadas automaticamente: {quantidade_fechada}"
)

app = App()
app.mainloop()
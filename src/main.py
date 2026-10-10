from database.conexao import inicializar_banco
from ui.app import App


inicializar_banco()

app = App()
app.mainloop()
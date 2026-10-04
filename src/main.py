from database.conexao import conectar, inicializar_banco
from models.categoria import Categoria

inicializar_banco()

categoria = Categoria(
    id=None,
    nome="Moradia",
    tipo="DESPESA",
    descricao="Gastos com aluguel, condomínio e contas da casa"
)

print(categoria)

conexao = conectar()

print("Banco inicializado e conexão realizada com sucesso.")

conexao.close()
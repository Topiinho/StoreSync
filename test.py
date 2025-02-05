# from datetime import datetime
from app.models.Produto import listar_produtos
from app.models.Produto import cadastrar_produto
from app.models.Fornecedor import listar_fornecedor
from app.models.Fornecedor import cadastrar_fornecedor
# from app.models.Transacao import compra

# data :str = datetime.now()
# data = data.strftime("%d/%m/%Y %H:%M:%S")
# print("Data e hora formatada:", data)


cadastrar_produto("Johnny", "Tom", 24, 13, "1", "1")
cadastrar_produto("Addie", "Jesse", 18, 10, "1", "1")
cadastrar_produto("Fannie", "Hattie", 18, 37, "1", "1")
cadastrar_produto("Jacob", "Rosalie", 4, 50, "5", "1")

cadastrar_fornecedor("Francis Rodriguez", "557817798")
cadastrar_fornecedor("Herbert Clarke", "4157360950")
cadastrar_fornecedor("Rosalie Marsh", "3124438918")
cadastrar_fornecedor("Matilda McDaniel", "1524577529")

listar_produtos("Todos", "a")
print("-----------------------------------------------")
listar_fornecedor("Todos", "a")

# compra(3, 4, 50, 220, data)
